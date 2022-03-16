import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DEFAULT_DB_NAME = 'models/db.sqlite'
DATABASE_NAME = os.getenv('DB_URL', DEFAULT_DB_NAME)
DATABASE_ECHO = False  # True for DB queries console output

engine = create_engine(f"sqlite:///{DATABASE_NAME}", echo=DATABASE_ECHO, future=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
