from fastapi import FastAPI
from .controllers import user_controller
from .database.user_database import init_db

app = FastAPI(title="User Service API", version="1.0.0")
app.include_router(user_controller.router)

@app.get("/")
def root():
    init_db()
    return {"message": "User Service is running"}