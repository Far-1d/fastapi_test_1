from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import Setting

SQL_DB_URL = f"""{Setting.DB_HOSTNAME}://{Setting.DB_USERNAME}:{Setting
    .DB_PASSWORD}@{Setting.DB_URL}:{Setting.DB_PORT}/{Setting.DB_NAME}"""

engine = create_engine(SQL_DB_URL)
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
