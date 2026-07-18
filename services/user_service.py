from sqlmodel import Session
from services.base_service import BaseService
from repository.user_repository import UserRepository
import pandas as pd

class UserService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)
        self.repo = UserRepository(self.session)

    def get_all_without_current_user(self, user_id: int):
        data, columns_names = self.repo.get_all_without_current_user(user_id)
        df = pd.DataFrame(data, columns=columns_names)
        return df

    def authenticate(self, obj):
        return self.repo.authenticate(obj)
