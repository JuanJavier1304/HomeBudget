from sqlmodel import Session, select
from models import Transaction, Category, Subcategory, PaymentMethod, TransactionType, TransactionVariability, TransactionVariability, TransactionParticipant, User, Transfer
from .base_repository import BaseRepository
from utils.convert import sqlmodel_to_df, list_to_df
import datetime
from sqlalchemy.sql.functions import concat
from sqlalchemy.orm import aliased

class TransferRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session)

