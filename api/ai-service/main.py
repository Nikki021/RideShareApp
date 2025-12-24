from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controllers import ai_controller

app = FastAPI(title="AI Service API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_controller.router)

@app.get("/")
def root():
    return {"message": "AI Service is running"}