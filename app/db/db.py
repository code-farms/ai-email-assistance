from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os

from app.db.models import Email, User

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    try:
        SQLModel.metadata.create_all(engine)

        with engine.connect() as conn:
            print("✅ Database connected and tables created successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
