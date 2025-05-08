from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#specify the connection string
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-adddress/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123456@localhost/FastAPI_db'

#create engine engine = enables sqlalchemy to connect to postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)
 
#create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#define a base class
Base = declarative_base()