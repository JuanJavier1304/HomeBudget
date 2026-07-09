from sqlmodel import Session
from services.base_service import BaseService
from repository.user_repository import UserRepository

class UserService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)
        self.repo = UserRepository(self.session)

    def get_all_without_current_user(self, user_id: int):
        return self.repo.get_all_without_current_user(user_id)

    def authenticate(self, obj):
        return self.repo.authenticate(obj)
