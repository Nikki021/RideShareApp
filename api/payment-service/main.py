from fastapi import FastAPI
from .controllers import payment_controller

app = FastAPI(title="Payment Service API", version="1.0.0")
app.include_router(payment_controller.router)

@app.get("/")
def root():
    return {"message": "Payment Service is running"}
