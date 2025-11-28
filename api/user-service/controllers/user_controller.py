from datetime import datetime, timezone
from ..models.user_model import UserCreate
from ..service.user_service import UserService
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()

@router.post("/register")
def register_user(user_create: UserCreate):
    if user_service.get_user_by_email(user_create.email):
        return {"error": "User already exists"}
    new_user = user_service.create_user(user_create)
    return {"message": "User registered successfully", 
            "user_details": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                "created_at": new_user.created_at,
                "role": new_user.role
            }
            }

@router.get("/{user_id}")
def get_user(user_id: str):
    user = user_service.users.get(user_id)
    if not user:
        return {"error": "User not found"}
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at,
        "role": user.role
    }

@router.put("/{user_id}")
def update_user(user_id: str, user_update: UserCreate):
    user = user_service.users.get(user_id)
    if not user:
        return {"error": "User not found"}
    user = user_service.update_user(user_id, user_update)
    return {"message": "User updated successfully", 
            "user_details": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "updated_at": user.updated_at,
                "role": user.role
            }
            }

@router.delete("/{user_id}")
def delete_user(user_id: str):
    success = user_service.delete_user(user_id)
    if not success:
        return {"error": "User not found"}
    return {"message": "User deleted successfully"}

@router.post("/login")
def login_user(email: str, password: str):
    user = user_service.login_user(email, password)
    if not user:
        return {"error": "Invalid email or password"}
    return {"message": "Login successful", 
            "user_details": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
            }