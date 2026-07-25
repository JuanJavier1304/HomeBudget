from sqlmodel import Session
from services.base_service import BaseService
from repository.account_holder_repository import AccountHolderRepository
import pandas as pd
import streamlit as st

class AccountHolderService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)
        self.repo = AccountHolderRepository(self.session)

    def get_account_holders(self, user_id):
        data, columns_names = self.repo.get_account_holders(user_id)
        df_account_holders = pd.DataFrame(data, columns=columns_names)

        columns_dataframe_config = {
            "id": None,
            "firstname": st.column_config.Column("Nombre"),
            "lastname": st.column_config.Column("Apellido"),
            "relationship": st.column_config.Column("Relación"),
            "opening_balance": st.column_config.NumberColumn("Balance apertura", format="S/%.2f")
        }
        
        columns_order = [
            "id",
            "firstname",
            "lastname",
            "relationship",
            "opening_balance"
        ]
        return df_account_holders, columns_dataframe_config, columns_order


    def get_account_holder_by_id(self, account_holder_id):
        data = self.repo.get_account_holder_by_id(account_holder_id)
        #df_account_holders = pd.DataFrame(data, columns=columns_names)
        return data
