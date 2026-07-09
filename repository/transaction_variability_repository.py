from sqlmodel import Session, select
from models import TransactionVariability
from .base_repository import BaseRepository
from utils.convert import sqlmodel_to_df

class TransactionVariabilityRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session)

