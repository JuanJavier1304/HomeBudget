# HomeBudget

Aplicación web para gestión de finanzas personales y gastos compartidos.

## Stack

- Python
- Streamlit
- PostgreSQL (Neon)
- GitHub

## Roadmap

- [x] Estructura inicial
- [x] Navegación multipágina
- [ ] Conexión a PostgreSQL
- [ ] Registro de gastos
- [ ] Registro de ingresos
- [ ] Dashboard
- [ ] Gastos compartidos


## Estructura tentativa
homebudget/
│
├── app.py
├── .env
├── requirements.txt
│
├── database/
│   ├── engine.py
│   ├── session.py
│   ├── models.py          # importa todos los modelos
│   └── init_db.py
│
├── models/
│   ├── user.py
│   ├── category.py
│   ├── subcategory.py
│   ├── account.py
│   ├── payment_method.py
│   ├── transaction.py
│   ├── transaction_share.py
│   ├── transfer.py
│   └── transfer_detail.py
│
├── repositories/
│   ├── user_repository.py
│   ├── category_repository.py
│   ├── transaction_repository.py
│   ├── transfer_repository.py
│   └── report_repository.py
│
├── services/
│   ├── balance_service.py
│   ├── transfer_service.py
│   ├── transaction_service.py
│   └── dashboard_service.py
│
├── pages/
│   ├── dashboard.py
│   ├── monthly_expenses.py
│   ├── transactions.py
│   ├── transfers.py
│   ├── categories.py
│   └── settings.py
│
├── components/
│   ├── aggrid.py
│   ├── sidebar.py
│   ├── dialogs.py
│   ├── metrics.py
│   └── forms.py
│
├── utils/
│   ├── auth.py
│   ├── constants.py
│   ├── formatters.py
│   └── validators.py
│
└── assets/