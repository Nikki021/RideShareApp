from fastapi import FastAPI
from .controllers import ride_request_controller
from .database.ride_database import init_db

app = FastAPI(title="Ride Service API", version="1.0.0")
app.include_router(ride_request_controller.router)

@app.get("/")
def root():
    init_db()
    return {"message": "Ride Service is running"}