from fastapi import FastAPI
from .controllers import user_controller

app = FastAPI(title="User Service API", version="1.0.0")
app.include_router(user_controller.router)

@app.get("/")
def root():
    return {"message": "User Service is running"}