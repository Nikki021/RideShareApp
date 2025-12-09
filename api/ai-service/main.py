from fastapi import FastAPI
from .controllers import ai_controller

app = FastAPI(title="AI Service API", version="1.0.0")
app.include_router(ai_controller.router)

@app.get("/")
def root():
    return {"message": "AI Service is running"}