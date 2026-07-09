from pandas.core.reshape import concat
from sqlmodel import Session, select
from models import User
from .base_repository import BaseRepository
from utils.convert import sqlmodel_to_df, list_to_df
from sqlalchemy.sql.functions import concat
import bcrypt

class UserRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session)

    def authenticate(self, obj):
        """
        Autenticar el inicio de sesión
        :return
            id y firstname del usuario
        """

        statement = (
            select(User.id, User.firstname, User.password_hash).where(User.username == obj.username)
        )
        user = self.session.exec(statement).first()

        # Si no encuentra el usuario, retorna None
        if not user:
            return None

        # Verifica la contraseña usando los atributos del objeto mapeado
        if bcrypt.checkpw(
                obj.password_hash.encode(),
                user.password_hash.encode()
        ):
            # Retorna la tupla que esperaba tu código original
            return user

        return None

    def get_all_without_current_user(self, user_id: int):
        """
        Verificar si categoría existe buscándolo por nombre
        :param category_name: Nombre de la categoria
        :return: True si existe, None si no
        """
        statement = (
            select(User.id,concat(User.firstname, " ", User.lastname).label("fullname"))
			.where(
                User.is_enable == "1",
                User.id != user_id
            )
        )

        result = self.session.exec(statement)
        columns_names = list(result.keys())
        df = list_to_df(result, columns_names)
        return df
