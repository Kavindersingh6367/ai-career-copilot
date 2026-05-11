from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl": {
            "ca": r"E:\python porjects\isrgrootx1.pem"
        }
    }
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

try:
    connection = engine.connect()
    print("Connected Successfully!")
except Exception as e:
    print("Error:", e)