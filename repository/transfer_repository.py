from .base_repository import BaseRepository

class TransferRepository(BaseRepository):

    def __init__(self, session):
        super().__init__(session)

