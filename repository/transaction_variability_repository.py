from .base_repository import BaseRepository

class TransactionVariabilityRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session)

