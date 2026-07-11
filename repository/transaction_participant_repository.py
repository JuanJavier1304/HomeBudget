from sqlmodel import Session, select
from models import TransactionParticipant
from .base_repository import BaseRepository
from utils.convert import sqlmodel_to_df

class TransactionParticipantRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session)

    def get_transaction_participants(self, user_id_princ: int, transaction_id: int):
        """
        Lista los participantes de la transaccion
        Args:
            user_id (int): ID del usuario dueño de la transaccion
            transaction_id (int): ID de la transaccion
        :return
            dataframe de los participantes
        """
        statement = (
            select(TransactionParticipant)
            .where(
                TransactionParticipant.transaction_id == transaction_id,
                TransactionParticipant.user_id != user_id_princ
            )
        )

        result = self.session.exec(statement).first()
        return sqlmodel_to_df(result)


    def updateFromTransaction(self, obj):

        db_obj = self.session.exec(
            select(TransactionParticipant).where(
                TransactionParticipant.transaction_id == obj.transaction_id,
                TransactionParticipant.user_id == obj.user_id
            )
        ).first()

        if db_obj:
            db_obj.assigned_amount = obj.assigned_amount
        else:
            self.session.add(obj)

        self.session.commit()

        if db_obj:
            self.session.refresh(db_obj)
            return db_obj

        self.session.refresh(obj)
        return obj