from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Date, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the base class for ORM models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, index=True)          # UUID length
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)         # use callable
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    dob = Column(Date, nullable=False)
    role = Column(String(20), nullable=False)                      # 'rider' or 'driver'
    is_logged_in = Column(Boolean, default=False, nullable=False)

# Database connection URL (update this as per your database configuration)
DATABASE_URL = "mysql+pymysql://root:Nikhil%40021@localhost:3306/rideapp"  # Example: SQLite database

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize the database (create tables)
def init_db():
    Base.metadata.create_all(bind=engine)

def store_user(db_session, user):
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user