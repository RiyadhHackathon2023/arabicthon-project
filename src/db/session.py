import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
load_dotenv()

url = URL.create(
    drivername="postgresql",
    username=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    host=os.getenv('POSTGRES_HOST'),
    database=os.getenv('POSTGRES_DB'),
    port=5432
)
print(url)
def get_engine():
    engine = create_engine(url)
    return engine

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
