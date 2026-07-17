from .base_repository import BaseRepository
from sqlalchemy.orm import aliased
from sqlalchemy import func, select, extract, and_
from models import Transfer, User
from sqlalchemy.sql.functions import concat

class TransferRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session)

    def get_previously_transfer(self):
        User_1 = aliased(User, name="from")
        User_2 = aliased(User, name="to")
        statement = (
            select(
                Transfer.id,
                concat(User_1.firstname, " ", User_1.lastname).label("user_name_from"),
                concat(User_2.firstname, " ", User_2.lastname).label("user_name_to"),
                Transfer.amount_transfer,
                Transfer.date_transfer,
                Transfer.comment
            )
    		.outerjoin(User_1, Transfer.id_user_from == User_1.id)
            .outerjoin(User_2, Transfer.id_user_to == User_2.id)
        )
        column_names = list(statement.selected_columns.keys())
        result = self.session.exec(statement).fetchall()
        return result, column_names
