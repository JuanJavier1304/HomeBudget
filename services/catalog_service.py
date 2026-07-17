from sqlmodel import Session
from services.base_service import BaseService
from repository.category_repository import CategoryRepository
from repository.subcategory_repository import SubcategoryRepository
from repository.payment_method_repository import PaymentMethodRepository
from repository.transaction_type_repository import TransactionTypeRepository
from repository.transaction_variability_repository import TransactionVariabilityRepository
from repository.date_interval_repository import DateIntervalRepository

class CatalogService(BaseService):
    def __init__(self, session: Session):
        super().__init__(session)
        # Opcional: Si tus repositorios específicos tienen métodos únicos, los instancias aquí.
        # Si solo usan get_all, puedes usar directamente un BaseRepository genérico.
        self.cat_repo = CategoryRepository(self.session)
        self.sub_repo = SubcategoryRepository(self.session)
        self.pay_repo = PaymentMethodRepository(self.session)
        self.type_repo = TransactionTypeRepository(self.session)
        self.var_repo = TransactionVariabilityRepository(self.session)
        self.dt_interval_repo = DateIntervalRepository(self.session)

    def get_catalog(self, model_class, repo_attr: str):
        """Obtiene de forma dinámica los datos usando el repositorio adecuado."""
        repo = getattr(self, repo_attr)
        return repo.get_all(model_class)
