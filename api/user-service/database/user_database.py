from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, Date, DateTime, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

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
    try:
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    except IntegrityError:
        db_session.rollback()
        raise

def get_user_by_id(db_session, user_id):
    return db_session.query(User).filter(User.id == user_id).first()

def get_user_by_email(db_session, email):
    return db_session.query(User).filter(User.email == email).first()

def get_all_users(db_session):
    return db_session.query(User).all()

def update_user(db_session, user_id, updated_fields: dict):
    user = get_user_by_id(db_session, user_id)
    if not user:
        return None
    allowed = {"username", "email", "hashed_password", "dob", "role", "is_logged_in"}
    for key, val in updated_fields.items():
        if key in allowed:
            setattr(user, key, val)
    # update timestamp
    user.updated_at = datetime.now(timezone.utc)
    try:
        db_session.commit()
        db_session.refresh(user)
        return user
    except IntegrityError:
        db_session.rollback()
        raise

def delete_user(db_session, user_id):
    user = get_user_by_id(db_session, user_id)
    if not user:
        return False
    try:
        db_session.delete(user)
        db_session.commit()
        return True
    except Exception:
        db_session.rollback()
        raise

def update_user_login_status(db_session, user_id, is_logged_in: bool):
    user = get_user_by_id(db_session, user_id)
    if not user:
        return None
    user.is_logged_in = bool(is_logged_in)
    user.updated_at = datetime.now(timezone.utc)
    try:
        db_session.commit()
        db_session.refresh(user)
        return user
    except IntegrityError:
        db_session.rollback()
        raise