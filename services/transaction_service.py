from sqlmodel import Session
from services.base_service import BaseService
from repository.transaction_repository import TransactionRepository
from collections import defaultdict
import pandas as pd
import streamlit as st

class TransactionService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)
        self.repo = TransactionRepository(self.session)

    def get_by_date_range(self, user_id: int, start_date, end_date):
        columns_dataframe_config = {
            "id": st.column_config.Column("ID", help="Identificador único"),
            "transaction_date": st.column_config.DateColumn("Fecha de Transacción"),
            "transaction_type_name": st.column_config.Column("Tipo Transacción"),
            "description": st.column_config.Column("Descripción"),
            "category_name": st.column_config.Column("Categoría"),
            "subcategory_name": st.column_config.Column("Subcategoría"),
            "amount": st.column_config.NumberColumn("Monto", format="S/%.2f"),  # Formatea como dinero si aplica
            "payment_method_name": st.column_config.Column("Método Pago"),
            "transaction_variability_name": st.column_config.Column("Fijo/Variable"),
            "comment": st.column_config.Column("Comentario"),
            "is_household_expense": st.column_config.Column("Es gasto de hogar"),
        }
        data, columns_names = self.repo.get_transactions_by_date_range(user_id, start_date, end_date)
        df = pd.DataFrame(data, columns=columns_names)
        return df, columns_dataframe_config

    def get_by_id(self, user_id: int, transaction_id: int):
        data = self.repo.get_transaction_by_id(user_id, transaction_id)
        return data

    def get_shared_transactions(self):
        # Muestra los gastos compartidos
        columns_dataframe_config = {
            "id": None,
            "transaction_date": st.column_config.DateColumn("Fecha de Transacción", format="YYYY-MM-DD"),
            "fullname_princ": st.column_config.Column("¿Quién pagó?"),
            "description": st.column_config.Column("Descripción"),
            "category_name": st.column_config.Column("Categoría"),
            "subcategory_name": st.column_config.Column("Subcategoría"),
            "amount": st.column_config.NumberColumn("Monto", format="S/%.2f"),
            "fullname_sec": st.column_config.Column("Devuelve"),
            "assigned_amount": st.column_config.NumberColumn("Monto a devolver", format="S/%.2f"),
            "comment": st.column_config.Column("Comentario"),
            "is_household_expense": None,
            "id_user_princ": None,
            "id_user_sec": None
        }
        columns_order = [
            "id",
            "transaction_date",
            "description",
            "category_name",
            "subcategory_name",
            "amount",
            "fullname_princ",
            "fullname_sec",
            "assigned_amount",
            "comment"
        ]
        df_transactions = self.repo.get_shared_transactions()
        return df_transactions, columns_dataframe_config, columns_order

    def update_transaction_by_transfer(self, obj):
        return self.repo.update_transaction_by_transfer(obj)

    def get_household_balance(self):
        df = self.repo.get_shared_transactions()

        balances = defaultdict(lambda: {
            "user_id": None,
            "username": None,
            "debt": 0,
            "balance": 0
        })

        for _, row in df.iterrows():
            payer = row["id_user_princ"]
            participant = row["id_user_sec"]
            assigned = row["assigned_amount"]

            # quien pagó debe recibir
            balances[payer]["user_id"] = payer
            balances[payer]["username"] = row["fullname_princ"]
            balances[payer]["balance"] += assigned

            # quien debe pagar
            balances[participant]["user_id"] = participant
            balances[participant]["username"] = row["fullname_sec"]
            balances[participant]["balance"] -= assigned
            balances[participant]["debt"] += row["assigned_amount"]

        return pd.DataFrame(balances.values())

    def get_transactions_by_month(self, user_id, year, month):
        data = self.repo.get_transactions_by_month(user_id,year,month)
        if not data:
            return pd.DataFrame(), {}, []

        # 2. Convertir la lista de filas mapeadas a DataFrame
        columns_dataframe_config = {
            "id": None,
            "transaction_date": st.column_config.DateColumn("Fecha de Transacción",format="YYYY-MM-DD"),
            "transaction_type_id": None,
            "transaction_type_name": st.column_config.Column("Tipo Transacción"),
            "description": st.column_config.Column("Descripción"),
            "category_id": None,
            "category_name": st.column_config.Column("Categoría"),
            "subcategory_id": None,
            "subcategory_name": st.column_config.Column("Subcategoría"),
            "amount": None,
            "real_amount": None,
            "final_amount": st.column_config.NumberColumn("Monto", format="S/%.2f"),  # Formatea como dinero si aplica
            "payment_method_id": None,
            "payment_method_name": st.column_config.Column("Método Pago"),
            "transaction_variability_id": None,
            "transaction_variability_name": st.column_config.Column("Fijo/Variable"),
            "comment": st.column_config.Column("Comentario"),
            "is_household_expense": st.column_config.Column("Es gasto de hogar"),
            "date_interval_name": st.column_config.Column("Intervalo")
        }
        columns_order = [
            "transaction_date",
            "transaction_type_name",
            "description",
            "category_name",
            "subcategory_name",
            "final_amount",
            "payment_method_name",
            "transaction_variability_name",
            "comment",
            "is_household_expense",
            "date_interval_name"
        ]
        df = pd.DataFrame([row._mapping for row in data])
        return df, columns_dataframe_config, columns_order

    def calculare_balance(self, df):
        """
        Calcula ingresos, gastos y balance agrupando dinámicamente por tipo de transacción.
        """
        if df.empty or "transaction_type_name" not in df.columns or "final_amount" not in df.columns:
            return 0.0, 0.0, 0.0

        # 1. Agrupar por tipo de transacción y sumar los montos
        df_summary = df.groupby("transaction_type_id")["final_amount"].sum()

        # 2. Extraer los valores buscando variaciones comunes de nombres (insensible a mayúsculas/minúsculas)
        total_income = 0.0
        total_expense = 0.0

        for id, monto in df_summary.items():
            if id == 1: # Si es gasto
                total_expense += float(monto)
            elif id == 2: # Si es ingreso
                total_income += float(monto)

        # 3. Calcular la diferencia neta
        balance = total_income - total_expense

        return total_income, total_expense, balance
