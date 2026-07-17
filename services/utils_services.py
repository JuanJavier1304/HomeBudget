from services.user_service import UserService
from database.connection import get_session

def rename_columns_df_excel():
    column_names = {
        "transaction_date": "Fecha de Transacción",
        "transaction_type_name": "Tipo Transacción",
        "description": "Descripción",
        "category_name": "Categoría",
        "subcategory_name": "Subcategoría",
        "final_amount": "Monto",
        "payment_method_name": "Método Pago",
        "transaction_variability_name": "Fijo/Variable",
        "comment": "Comentario",
        "is_shared": "Es compartido",
        "is_household_expense": "Es gasto de hogar",
    }
    return column_names


def rename_columns_df_transfer_excel():
    column_names = {
        "user_name_from": "De:",
        "user_name_to": "Para:",
        "amount_transfer": "Monto Transferencia",
        "date_transfer": "Fecha Transferencia",
        "comment": "Comentario"
    }
    return column_names
    

def authenticate_user(user):
    with get_session() as session:
        service = UserService(session)
        return service.authenticate(user)