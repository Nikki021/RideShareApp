from datetime import datetime, timezone
from ..models.user_model import User, UserCreate
import uuid
from ..security.hashing import hash_password, verify_password

class UserService:
    def __init__(self):
        self.users = {}  # In-memory user storage for demonstration

    def create_user(self, user_create: UserCreate) -> User:
        user_id = str(uuid.uuid4())
        hashed_password = hash_password(user_create.password)
        new_user = User(
            id=user_id,
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            dob=user_create.dob,
            role=user_create.role,
            is_logged_in=False
        )
        self.users[user_id] = new_user
        return new_user
    
    def get_user_by_id(self, user_id: str) -> User | None:
        return self.users.get(user_id)

    def get_user_by_email(self, user_email: str) -> User | None:
        for user in self.users.values():
            if user.email == user_email:
                return user
        return None
    
    def update_user(self, user_id: str, user_update: UserCreate) -> User | None:
        user = self.users.get(user_id)
        if user:
            user.username = user_update.username
            user.email = user_update.email
            user.hashed_password = hash_password(user_update.password)
            user.dob = user_update.dob
            user.role = user_update.role
            user.updated_at = datetime.now(timezone.utc)
            return user
        return None
    
    def delete_user(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
    
    def login_user(self, email: str, password: str) -> User | None:
        user = self.get_user_by_email(email)
        if user and verify_password(password, user.hashed_password):
            user.is_logged_in = True
            return {"message": "Login successful", "user_details": user}
        return {"error": "Invalid email or password"}
    
    def is_logged_in(self, user_id: str) -> bool:
        return self.get_user_by_id(user_id).is_logged_in if self.get_user_by_id(user_id) else False
    
    def logout_user(self, user_id: str):
        user = self.get_user_by_id(user_id)
        if user and user.is_logged_in:
            user.is_logged_in = False
            return {"message": "Logout successful"}
        return {"error": "User is not logged in"}