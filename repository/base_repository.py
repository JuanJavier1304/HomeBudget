from sqlmodel import Session, select
from utils.convert import sqlmodel_to_df

class BaseRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_all(self, obj):
        statement = (
            select(obj)
            .order_by(obj.id)
        )
        result = self.session.exec(statement).all()
        return sqlmodel_to_df(result)

    def get_by_id(self, obj, id: int):
        """
        Obtener por id
        :param id: ID del objeto
        :return: select by id
        """
        return self.session.get(obj, id)

    def insert(self, obj):
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj):
        merged_obj = self.session.merge(obj)
        self.session.commit()
        self.session.refresh(merged_obj)
        return merged_obj


    def delete(self, obj, id: int):
        try:
            # 1. Buscamos la categoría por ID en la sesión
            obj_buscar = BaseRepository.get_by_id(self, obj=obj, id=id)

            # 2. Si existe, la eliminamos y guardamos cambios
            if obj_buscar is not None:
                self.session.delete(obj_buscar)
                self.session.commit()
                return True

            return False
        except Exception as e:
            self.session.rollback()
            return False