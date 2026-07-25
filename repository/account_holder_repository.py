from sqlmodel import Session, select
from models import AccountHolder
from .base_repository import BaseRepository

class AccountHolderRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session)

    def get_account_holders(self, user_id):
        """
        Obtiene todos los Account Holders pertenecientes al usuario
        """
        statement = (
            select(
                AccountHolder.id,
                AccountHolder.user_id,
                AccountHolder.firstname,
                AccountHolder.lastname,
                AccountHolder.relationship,
                AccountHolder.opening_balance
            )
            .where(
                AccountHolder.user_id == user_id,
                AccountHolder.is_enabled == True
            )
        )
        column_names = list(statement.selected_columns.keys())
        results = self.session.exec(statement).fetchall()
        return results, column_names

    
    def get_account_holder_by_id(self, account_holder_id):
        """
        Obtiene registro Account Holder por id
        """
        statement = (
            select(
                AccountHolder.id,
                AccountHolder.user_id,
                AccountHolder.firstname,
                AccountHolder.lastname,
                AccountHolder.relationship,
                AccountHolder.opening_balance
            )
            .where(
                AccountHolder.is_enabled == True,
                AccountHolder.id == account_holder_id
            )
        )
        column_names = list(statement.selected_columns.keys())
        results = self.session.exec(statement).fetchone()
        return results, column_names