from fastapi import FastAPI
from .controllers import ride_request_controller

app = FastAPI(title="Ride Service API", version="1.0.0")
app.include_router(ride_request_controller.router)

@app.get("/")
def root():
    return {"message": "Ride Service is running"}