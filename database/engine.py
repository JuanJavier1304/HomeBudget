# database/engine.py

import os
import models
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel

def inicializar_mapeadores():
    # Este llamado levanta la configuración interna de relaciones de SQLModel
    # impidiendo errores de inicialización perezosa.
    pass

load_dotenv()

DB_USER = os.getenv("PGUSER")
DB_PASSWORD = os.getenv("PGPASSWORD")
DB_HOST = os.getenv("PGHOST")
DB_PORT = os.getenv("PGPORT")
DB_NAME = os.getenv("PGDATABASE")

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)
