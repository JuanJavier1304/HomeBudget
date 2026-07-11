from sqlmodel import Session, select
from models import PaymentMethod
from .base_repository import BaseRepository

class PaymentMethodRepository (BaseRepository):

    def __init__(self, session):
        super().__init__(session)

    def get_payment_method_by_name(self, payment_method_name: str):
        """
        Verificar si el metodo de pago existe buscándolo por nombre
        :param payment_method_name: Nombre del metodo de pago
        :return: True si existe, None si no
        """
        statement = (
            select(PaymentMethod)
            .where(PaymentMethod.name == payment_method_name)
        )
        result = self.session.exec(statement).first()
        return result
