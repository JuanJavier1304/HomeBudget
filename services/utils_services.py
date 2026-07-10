
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