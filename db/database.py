from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


engine = create_engine("postgresql://postgres:password@localhost:5432/fafa")
session_maker = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
