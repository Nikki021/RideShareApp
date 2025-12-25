from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controllers import user_controller

app = FastAPI(title="User Service API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=False,  # Set to True only when using specific origins
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_controller.router)

@app.get("/")
def root():
    return {"message": "User Service is running"}