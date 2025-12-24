from datetime import datetime, date
from pydantic import BaseModel
from enum import Enum

class Role(str, Enum):
    DRIVER = "driver"
    RIDER = "rider"

class User(BaseModel):
    id: str
    username: str
    email: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    dob: date | None = None
    role: Role
    is_logged_in: bool = False

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    dob: date | None = None
    role: Role