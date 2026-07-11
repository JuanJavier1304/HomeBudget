from sqlmodel import select, func
from models import Subcategory
from .base_repository import BaseRepository
from utils.convert import sqlmodel_to_df

class SubcategoryRepository (BaseRepository):

    def __init__(self, session):
        super().__init__(session)

    def exists_subcategory_by_name(self, category_id: int, subcategory_name: str):
        """
        Conocer si existe subcategoría por nombre
        :param subcategory_name: nombre de subcategoría
        :param category_id: id de la categoría
        :return: si existe o no
        """
        statement = (
            select(Subcategory)
            .where(
                func.upper(Subcategory.name) == subcategory_name.upper(),
                Subcategory.category_id == category_id
            )
        )

        result = self.session.exec(statement).first()
        return result is not None


    def list_by_category(self, category_id: int):
        """
        Lista las subcategorias por categoría en la base de datos.
        :param category_id: id de la categoría
        :return: diccionario de datos result
        """
        statement = (
            select(Subcategory)
            .where(Subcategory.category_id == category_id)
        )

        result = self.session.exec(statement).all()
        return sqlmodel_to_df(result)
