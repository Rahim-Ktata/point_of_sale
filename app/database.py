
#------------ here we're just connecting to the db ---------------------

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# this is the main line u need to edit for a different db(sqlite..)
# SQLALCHEMY_DATABASE_URL = "postgresql://postgers:@postgresserver/db"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# echo = true : show executed sql queries in terminal
# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# use session as black box for now
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # a class we'll use later to create models
