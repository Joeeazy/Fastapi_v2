from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# from psycopg2.extras import RealDictCursor
# import psycopg2
# import time

#specify the connection string
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-adddress/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123456@localhost/FastAPI_db'

#create engine engine = enables sqlalchemy to connect to postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)
 
#create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#define a base class
Base = declarative_base()

#create a depandancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#connection to postgres DB using psycopg2 library
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database = 'FastAPI_db', user = 'postgres', password = '123456', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection Successful")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error", error)
#         time.sleep(2)