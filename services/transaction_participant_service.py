from sqlmodel import Session
from services.base_service import BaseService
from repository.transaction_participant_repository import TransactionParticipantRepository

class TransactionParticipantService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)
        self.repo = TransactionParticipantRepository(self.session)


    def get_transaction_participants(self, user_id: int, transaction_id: int):
        return self.repo.get_transaction_participants(user_id, transaction_id)


    def updateFromTransaction(self, obj):
        return self.repo.updateFromTransaction(obj)

