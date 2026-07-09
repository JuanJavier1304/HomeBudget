import streamlit as st
from sqlmodel import Session
from repository.base_repository import BaseRepository

class BaseService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = BaseRepository(session)

    def insert(self, entity):
        entity = self.repository.insert(entity)
        st.cache_data.clear()
        return entity

    def update(self, entity):
        entity = self.repository.update(entity)
        st.cache_data.clear()
        return entity

    def delete(self, model, entity_id):
        success = self.repository.delete(model, entity_id)
        if success:
            st.cache_data.clear()

        return success
