from sqlmodel import Session
from services.base_service import BaseService
from repository.date_interval_repository import DateIntervalRepository
from models import DateInterval
import pandas as pd
import streamlit as st

class DateIntervalService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)
        self.repo = DateIntervalRepository(self.session)

    def get_last_end_date_from_interval(self):
        """Trae la fecha de fin más reciente para sugerir la siguiente."""
        return self.repo.get_last_end_date_from_interval()
    
    def get_all(self):
        """Trae la fecha de fin más reciente para sugerir la siguiente."""
        data = self.repo.get_all(DateInterval)
        if data.empty:
            return pd.DataFrame(), {}, []

        # 2. Convertir la lista de filas mapeadas a DataFrame
        columns_dataframe_config = {
            "id": None,
            "name": st.column_config.Column("Nombre Periodo"),
            "start_date": st.column_config.DateColumn("Fecha de Inicio",format="YYYY-MM-DD"),
            "end_date": st.column_config.DateColumn("Fecha de Fin",format="YYYY-MM-DD"),
            "is_active": None,
            "created_at": None,
            "updated_at": None,
        }
        columns_order = [
            "start_date",
            "end_date",
            "name",
        ]
        
        return data, columns_dataframe_config, columns_order

    