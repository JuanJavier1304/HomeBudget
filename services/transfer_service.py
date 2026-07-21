import streamlit as st
from sqlmodel import Session
from services.base_service import BaseService
from repository.transfer_repository import TransferRepository
import pandas as pd
import streamlit as st

class TransferService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)
        self.repo = TransferRepository(self.session)

    def get_previously_transfer(self):
        data, columns_names = self.repo.get_previously_transfer()
        df_transfer = pd.DataFrame(data, columns=columns_names)
        
        columns_dataframe_config = {
            "id": None,
            "user_name_from": st.column_config.Column("De:"),
            "user_name_to": st.column_config.Column("Para:"),
            "amount_transfer": st.column_config.NumberColumn("Monto", format="S/%.2f"),
            "date_transfer": st.column_config.DateColumn("Fecha de Transferencia", format="YYYY-MM-DD"),
            "comment": st.column_config.Column("Comentario")
        }
        
        columns_order = [
            "id",
            "date_transfer",
            "user_name_from",
            "user_name_to",
            "amount_transfer",
            "comment"
        ]
        return df_transfer, columns_dataframe_config, columns_order

    def get_transfer_by_id(self, transfer_id):
        data = self.repo.get_transfer_by_id(int(transfer_id))
        return data