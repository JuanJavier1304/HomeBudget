from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel.main import default_registry

# === TRUCO PARA STREAMLIT (HOT-RELOAD) ===
# Limpia el registro viejo de SQLAlchemy en cada recarga de página, evitando el error de "failed to locate a name" y mappers duplicados.
default_registry.dispose()

# ==========================================
# MODELO: CATEGORY
# ==========================================
class Category(SQLModel, table=True):
    __tablename__ = "category"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, sa_column_kwargs={"unique": True})

    # Relaciones
    subcategories: List["Subcategory"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    transactions: List["Transaction"] = Relationship(back_populates="category")


# ==========================================
# MODELO: SUBCATEGORY
# ==========================================
class Subcategory(SQLModel, table=True):
    __tablename__ = "subcategory"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    category_id: int = Field(foreign_key="category.id")
    name: str = Field(max_length=30)

    # Relaciones
    category: Optional["Category"] = Relationship(
        back_populates="subcategories"
        #sa_relationship_kwargs = {"back_populates": "subcategories"}
    )
    transactions: List["Transaction"] = Relationship(back_populates="subcategory")

# ==========================================
# MODELO: PAYMENT METHOD
# ==========================================

class PaymentMethod(SQLModel, table=True):
    __tablename__ = "payment_method"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, sa_column_kwargs={"unique": True})

    # Relaciones
    transactions: List["Transaction"] = Relationship(back_populates="payment_method")


# ==========================================
# MODELO: TRANSACTION_TYPE
# ==========================================
class TransactionType(SQLModel, table=True):
    __tablename__ = "transaction_type"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, sa_column_kwargs={"unique": True})

    # Relaciones
    transactions: List["Transaction"] = Relationship(back_populates="transaction_type")


# ==========================================
# MODELO: TRANSACTION_VARIABILITY
# ==========================================
class TransactionVariability(SQLModel, table=True):
    __tablename__ = "transaction_variability"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=30, sa_column_kwargs={"unique": True})

    # Relaciones
    transactions: List["Transaction"] = Relationship(back_populates="transaction_variability")


# ==========================================
# MODELO: USERS
# ==========================================
class User(SQLModel, table=True):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: str = Field(max_length=8, sa_column_kwargs={"unique": True})
    firstname: str = Field(max_length=20)
    lastname: str = Field(max_length=20)
    date_created: datetime = Field(default_factory=datetime.utcnow)
    is_enable: str = Field(default="1", max_length=1)
    username: str = Field(max_length=30)
    password_hash: Optional[str] = Field(default=None, max_length=100)

    # Relaciones
    transactions: List["Transaction"] = Relationship(back_populates="user")
    participants: List["TransactionParticipant"] = Relationship(back_populates="user")
    transfers_sent: List["Transfer"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Transfer.id_user_from]"},
        back_populates="user_from"
    )
    transfers_received: List["Transfer"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Transfer.id_user_to]"},
        back_populates="user_to"
    )

# ==========================================
# MODELO: TRANSACTION PARTICIPANT
# ==========================================
class TransactionParticipant(SQLModel, table=True):
    __tablename__ = "transaction_participant"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_id: int = Field(foreign_key="transaction.id")
    user_id: int = Field(foreign_key="user.id")
    assigned_amount: Optional[Decimal] = None

    # Relaciones
    transaction: Optional["Transaction"] = Relationship(back_populates="participants")
    user: Optional["User"] = Relationship(back_populates="participants")

# ==========================================
# MODELO: TRANSACTION
# ==========================================
class Transaction(SQLModel, table=True):
    __tablename__ = "transaction"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    date_created: datetime = Field(default_factory=datetime.utcnow)
    transaction_date: date
    transaction_type_id: int = Field(foreign_key="transaction_type.id")
    description: str = Field(max_length=100)
    category_id: int = Field(foreign_key="category.id")
    subcategory_id: Optional[int] = Field(default=None, foreign_key="subcategory.id")
    amount: Decimal
    payment_method_id: int = Field(foreign_key="payment_method.id")
    transaction_variability_id: int = Field(foreign_key="transaction_variability.id")
    comment: Optional[str] = Field(default=None, max_length=150)
    is_shared: Optional[bool] = None
    is_household_expense: Optional[bool] = None
    transfer_id: Optional[int] = Field(default=None, foreign_key="transfer.id")
    real_amount: Decimal

    # Relaciones
    user: Optional["User"] = Relationship(back_populates="transactions")
    category: Optional["Category"] = Relationship(back_populates="transactions")
    subcategory: Optional["Subcategory"] = Relationship(back_populates="transactions")
    payment_method: Optional["PaymentMethod"] = Relationship(back_populates="transactions")
    participants: List["TransactionParticipant"] = Relationship(back_populates="transaction")
    transfer: Optional["Transfer"] = Relationship(back_populates="transactions")
    transfer_details: List["TransferDetail"] = Relationship(back_populates="transaction")
    transaction_type: Optional["TransactionType"] = Relationship(back_populates="transactions")
    transaction_variability: Optional["TransactionVariability"] = Relationship(back_populates="transactions")


# ==========================================
# MODELO: TRANSFER
# ==========================================
class Transfer(SQLModel, table=True):
    __tablename__ = "transfer"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    id_user_from: int = Field(foreign_key="user.id")
    id_user_to: int = Field(foreign_key="user.id")
    amount_transfer: Decimal
    date_transfer: date
    date_created: datetime = Field(default_factory=datetime.utcnow)
    comment: Optional[str] = None

    # Relaciones
    user_from: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Transfer.id_user_from]"})
    user_to: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Transfer.id_user_to]"})
    transactions: List["Transaction"] = Relationship(back_populates="transfer")
    details: List["TransferDetail"] = Relationship(back_populates="transfer")


# ==========================================
# MODELO: TRANSFER DETAIL
# ==========================================
class TransferDetail(SQLModel, table=True):
    __tablename__ = "transfer_detail"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)

    transfer_id: int = Field(foreign_key="transfer.id")
    transaction_id: int = Field(foreign_key="transaction.id")
    amount_applied: Optional[Decimal] = None

    #Relaciones
    transfer: Optional["Transfer"] = Relationship(back_populates="details")
    transaction: Optional["Transaction"] = Relationship(back_populates="transfer_details")


# ==========================================
# MODELO: DATE_INTERVAL
# ==========================================
class DateInterval(SQLModel, table=True):
    __tablename__ = "date_interval"
    __table_args__ = {'extend_existing': True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    start_date: date
    end_date: date
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    

try:
    User.model_rebuild()
    TransactionParticipant.model_rebuild()
except AttributeError:
    # Si usas una versión antigua, caerá aquí y usará el método clásico
    User.update_forward_refs()
    TransactionParticipant.update_forward_refs()