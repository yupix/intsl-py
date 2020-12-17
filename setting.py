from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Engine = create_engine('sqlite:///data/database/server.db', encoding="utf-8")  # DEBUG時のみecho=True

Session = sessionmaker(bind=Engine)

session = Session()
Base = declarative_base()
