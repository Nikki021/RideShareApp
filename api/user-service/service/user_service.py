from datetime import datetime, timezone
from ..models.user_model import User, UserCreate
import uuid
from ..security.hashing import hash_password, verify_password
from ..database.user_database import SessionLocal, store_user, get_user_by_id, get_user_by_email, get_all_users, update_user, delete_user, update_user_login_status

class UserService:
    def __init__(self):
        self.users = {}  # In-memory user storage for demonstration
        self.db = SessionLocal()

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
        # self.users[user_id] = new_user
        # store the created user in the database
        store_user(self.db, new_user)
        return new_user
    
    def get_user_by_id(self, user_id: str) -> User | None:
        return get_user_by_id(self.db, user_id)

    def get_user_by_email(self, user_email: str) -> User | None:
        return get_user_by_email(self.db, user_email)
    
    def update_user(self, user_id: str, user_update: UserCreate) -> User | None:
        updated_fields = {
            "username": user_update.username,
            "email": user_update.email,
            "hashed_password": hash_password(user_update.password),
            "dob": user_update.dob,
            "role": user_update.role
        }
        return update_user(self.db, user_id, updated_fields)
    
    def delete_user(self, user_id: str) -> bool:
        return delete_user(self.db, user_id)
    
    def login_user(self, email: str, password: str) -> User | None:
        user = self.get_user_by_email(email)
        if user and verify_password(password, user.hashed_password):
            update_user_login_status(self.db, user.id, True)
            user.is_logged_in = True
            return {"message": "Login successful", "user_details": user}
        return {"error": "Invalid email or password"}
    
    def is_logged_in(self, user_id: str) -> bool:
        return self.get_user_by_id(user_id).is_logged_in if self.get_user_by_id(user_id) else False
    
    def logout_user(self, user_id: str):
        user = self.get_user_by_id(user_id)
        if user and user.is_logged_in:
            # update DB login status
            updated = update_user_login_status(self.db, user.id, False)
            if updated:
                # update local cache if present
                if hasattr(self, "users") and isinstance(self.users, dict):
                    self.users[updated.id] = updated
                return {"message": "Logout successful", "user_details": updated}
            # fallback: update in-memory object
            user.is_logged_in = False
            return {"message": "Logout successful", "user_details": user}
        return {"error": "User is not logged in"}