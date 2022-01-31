from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///app_event.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, ** {
	'connect_args': {
		'check_same_thread': False
	},
	'poolclass': StaticPool
	})

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

Base = declarative_base()


