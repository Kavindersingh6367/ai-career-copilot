from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get DATABASE_URL from .env (local) or Render Environment Variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set!")

# Get the absolute path of the current project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to SSL certificate
SSL_CERT_PATH = os.path.join(BASE_DIR, "isrgrootx1.pem")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "ssl": {
            "ca": SSL_CERT_PATH
        }
    }
)

# Create session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Test database connection
try:
    with engine.connect() as connection:
        print("✅ Connected to TiDB successfully!")
except Exception as e:
    print("❌ Database Connection Error:")
    print(e)