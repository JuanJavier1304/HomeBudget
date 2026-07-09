from sqlmodel import Session
from services.base_service import BaseService
from repository.transaction_repository import TransactionRepository # Tu repo específico

class TransferService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)
        self.repo = TransactionRepository(self.session)

