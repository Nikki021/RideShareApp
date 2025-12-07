from datetime import datetime, date
from pydantic import BaseModel

class User(BaseModel):
    id: str
    username: str
    email: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    dob: date | None = None
    role: str
    is_logged_in: bool = False

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    dob: date | None = None
    role: str