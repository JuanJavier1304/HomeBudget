from sqlmodel import Session, select
from models import DateInterval
from .base_repository import BaseRepository
from sqlalchemy import select, func

class DateIntervalRepository (BaseRepository):

    def __init__(self, session):
        super().__init__(session)

    def get_last_end_date_from_interval(self):
        statement = (
            select(
                func.max(DateInterval.end_date).label("end_date")
            )
            .where(
                DateInterval.is_active == True
            )
        )

        result = self.session.exec(statement).scalar()
        #columns_names = list(result.keys())
        #df = list_to_df(result, columns_names)
        return result