# database/create_db.py
from sqlmodel import SQLModel
from database.engine import engine
import models

def create_db():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db()