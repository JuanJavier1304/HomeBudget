from sqlmodel import Session, select
from models import Category
from .base_repository import BaseRepository
from utils.convert import sqlmodel_to_df

class CategoryRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session)

    def get_category_by_name(self, category_name: str):
        """
        Verificar si categoría existe buscándolo por nombre
        :param category_name: Nombre de la categoria
        :return: True si existe, None si no
        """
        statement = (
            select(Category)
            .where(Category.name == category_name)
        )

        results = self.session.exec(statement).first()
        return results
