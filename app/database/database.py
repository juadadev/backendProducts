import os
import time

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def wait_for_db(retries: int = 10, delay: int = 3):
    """Espera hasta que la base de datos esté disponible"""
    from sqlalchemy.exc import OperationalError

    for attempt in range(retries):
        try:
            # Intenta conectar
            with engine.connect() as conn:
                return
        except OperationalError:
            print(f"DB not ready, retrying {attempt + 1}/{retries}...")
            time.sleep(delay)
    raise RuntimeError("Cannot connect to the database after multiple attempts")


def create_database_and_table():
    Base.metadata.create_all(bind=engine)
