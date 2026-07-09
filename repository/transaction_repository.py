from sqlmodel import Session, select
from models import Transaction, Category, Subcategory, PaymentMethod, TransactionType, TransactionVariability, TransactionParticipant, User, Transfer
from .base_repository import BaseRepository
from utils.convert import sqlmodel_to_df, list_to_df
import datetime
from sqlalchemy.sql.functions import concat
from sqlalchemy.orm import aliased
from sqlalchemy import func, select, extract, and_

class TransactionRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session)

    def get_transactions_by_date_range(self, user_id:int, transaction_start_date: datetime, transaction_end_date: datetime):
        """
        Lista los movimientos por fecha
        Args:
            user_id (int): ID del usuario
            transaction_date (date): Fecha de la transaccion
        :return
            dataframe de las transacciones según fecha
        """
        statement = (
            select(
                Transaction.id,
                Transaction.transaction_date,
                TransactionType.name.label("transaction_type_name"),
                Transaction.description,
                Category.name.label("category_name"),
                Subcategory.name.label("subcategory_name"),
                Transaction.amount,
                PaymentMethod.name.label("payment_method_name"),
                TransactionVariability.name.label("transaction_variability_name"),
                Transaction.comment,
                Transaction.is_shared,
                Transaction.is_household_expense
        )
    		.outerjoin(Category, Transaction.category_id == Category.id)
    		.outerjoin(Subcategory, Transaction.subcategory_id == Subcategory.id)
    		.outerjoin(PaymentMethod, Transaction.payment_method_id == PaymentMethod.id)
    		.outerjoin(TransactionType, Transaction.transaction_type_id == TransactionType.id)
    		.outerjoin(TransactionVariability, Transaction.transaction_variability_id == TransactionVariability.id)
            .where(
				Transaction.transaction_date.between(transaction_start_date, transaction_end_date),
				Transaction.user_id == user_id
			)
            .order_by(Transaction.transaction_date.asc(), Transaction.id)
        )

        # Sin all()
        result = self.session.exec(statement)
        columns_names = list(result.keys())
        df = list_to_df(result, columns_names)

        return df

    def get_transaction_by_id(self, user_id: int, transaction_id: int):
        """
        Lista los movimientos por ID
        Args:
            user_id (int): ID del usuario
        :return
            dataframe de las transacciones por id
        """
        statement = (
            select(Transaction)
            .where(
                Transaction.id == transaction_id,
                Transaction.user_id == user_id
            )
        )

        # Sin all()
        result = self.session.exec(statement).first()
        return result

    def get_shared_transactions(self):
        """
        Lista de gastos compartidos
        :return
            dataframe de los gastos compartidos
        """
        # 1. Creamos los alias para identificar cada rol del usuario
        User_1 = aliased(User, name="princ")
        User_2 = aliased(User, name="sec")
        statement = (
            select(
                Transaction.id,
                Transaction.transaction_date,
                Transaction.description,
                Category.name.label("category_name"),
                Subcategory.name.label("subcategory_name"),
                Transaction.amount,
                Transaction.comment,
                User_1.username.label("fullname_princ"),
                User_1.id.label("id_user_princ"),
                User_2.username.label("fullname_sec"),
                User_2.id.label("id_user_sec"),
                #concat(User_1.firstname, " ", User_1.lastname).label("fullname_princ"),
                #concat(User_2.firstname, " ", User_2.lastname).label("fullname_sec"),
                TransactionParticipant.assigned_amount,
                Transaction.is_household_expense
            )
    		.outerjoin(Category, Transaction.category_id == Category.id)
    		.outerjoin(Subcategory, Transaction.subcategory_id == Subcategory.id)
    		.outerjoin(
                TransactionParticipant,
                (Transaction.id == TransactionParticipant.transaction_id) &
                (Transaction.user_id != TransactionParticipant.user_id)
            )
    		.outerjoin(User_1, Transaction.user_id == User_1.id)
            .outerjoin(User_2, TransactionParticipant.user_id == User_2.id)
            .where(
                #Transaction.user_id == user_id,
                #Transaction.is_shared == True
                Transaction.is_household_expense == True,
                Transaction.transfer_id == None
            )
            .order_by(Transaction.transaction_date.asc())
        )

        result = self.session.exec(statement)
        columns_names = list(result.keys())
        df = list_to_df(result, columns_names)

        return df

    def update_transaction_by_transfer(self, obj):
        merged_obj = self.session.get(Transaction, obj.id)

        merged_obj.transfer_id = obj.transfer_id
        merged_obj.real_amount = obj.real_amount

        self.session.add(merged_obj)
        self.session.commit()
        self.session.refresh(merged_obj)

        return merged_obj


    ############ PARA DASHBOARD ############
    def get_transactions_by_month(self, user_id: int, year: int, month: int):
        statement_1 = (
            select(
                Transaction.id,
                Transaction.transaction_date,
                Transaction.transaction_type_id,
                TransactionType.name.label("transaction_type_name"),
                Transaction.description,
                Transaction.category_id,
                Category.name.label("category_name"),
                Transaction.subcategory_id,
                Subcategory.name.label("subcategory_name"),
                Transaction.amount,
                Transaction.real_amount, # Monto real de la transacción
                Transaction.payment_method_id,
                PaymentMethod.name.label("payment_method_name"),
                Transaction.transaction_variability_id,
                TransactionVariability.name.label("transaction_variability_name"),
                Transaction.comment,
                Transaction.is_shared,
                Transaction.is_household_expense,
                func.coalesce(Transaction.real_amount, Transaction.amount).label("final_amount")
            )
            .outerjoin(Category, Transaction.category_id == Category.id)
            .outerjoin(Subcategory, Transaction.subcategory_id == Subcategory.id)
            .outerjoin(PaymentMethod, Transaction.payment_method_id == PaymentMethod.id)
            .outerjoin(TransactionType, Transaction.transaction_type_id == TransactionType.id)
            .outerjoin(TransactionVariability, Transaction.transaction_variability_id == TransactionVariability.id)
            .where(
                Transaction.user_id == user_id,
                extract('year', Transaction.transaction_date) == year,
                extract('month', Transaction.transaction_date) == month
            )
        )

        #result = self.session.exec(statement_1).fetchall()
        #return result

        # 2. Definir la segunda consulta (Nueva consulta con las mismas columnas)
        statement_2 = (
            select(
                Transaction.id,
                Transaction.transaction_date,
                Transaction.transaction_type_id,
                TransactionType.name.label("transaction_type_name"),
                Transaction.description,
                Transaction.category_id,
                Category.name.label("category_name"),
                Transaction.subcategory_id,
                Subcategory.name.label("subcategory_name"),
                Transaction.amount,
                TransactionParticipant.assigned_amount.label("real_amount"),
                Transaction.payment_method_id,
                PaymentMethod.name.label("payment_method_name"),
                Transaction.transaction_variability_id,
                TransactionVariability.name.label("transaction_variability_name"),
                Transaction.comment,
                Transaction.is_shared,
                Transaction.is_household_expense,
                func.coalesce(TransactionParticipant.assigned_amount, Transaction.amount).label("final_amount")
            )
            .join(Transfer, Transfer.id == Transaction.transfer_id)
            .outerjoin(
                TransactionParticipant,
                and_(
                    Transaction.id == TransactionParticipant.transaction_id,
                    TransactionParticipant.user_id == user_id
                )
            )
            # Mismos joins que el statement_1
            .outerjoin(Category, Transaction.category_id == Category.id)
            .outerjoin(Subcategory, Transaction.subcategory_id == Subcategory.id)
            .outerjoin(PaymentMethod, Transaction.payment_method_id == PaymentMethod.id)
            .outerjoin(TransactionType, Transaction.transaction_type_id == TransactionType.id)
            .outerjoin(TransactionVariability, Transaction.transaction_variability_id == TransactionVariability.id)
            # Condición de tu nueva consulta
            .where(
                Transaction.user_id != user_id,
                extract('year', Transaction.transaction_date) == year,
                extract('month', Transaction.transaction_date) == month
            )
        )

        # 3. Unir ambas consultas mediante UNION ALL y aplicar el ordenamiento final
        statement = statement_1.union_all(statement_2).order_by(Transaction.transaction_date.asc(), Transaction.id)

        # 4. Ejecutar y retornar
        result = self.session.exec(statement).fetchall()
        return result