import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_NAME = 'models/db.sqlite' if not os.environ.get('DB_URL') else os.environ['DB_URL']
DATABASE_ECHO = False  # True for DB queries console output

engine = create_engine(f"sqlite:///{DATABASE_NAME}", echo=DATABASE_ECHO, future=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)
