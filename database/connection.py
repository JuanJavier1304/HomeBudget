# database/connection.py

import os
import psycopg2
from dotenv import load_dotenv

#load_dotenv()
load_dotenv(override=True)

def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST"),
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        sslmode=os.getenv("PGSSLMODE")
    )
