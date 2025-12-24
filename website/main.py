from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="RideShare Web Application", version="1.0.0")

# Enable CORS for all origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=False,  # Set to True only when using specific origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# Mount static files
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

@app.get("/")
def read_root():
    """Serve the main HTML page"""
    return FileResponse(os.path.join(current_dir, "templates", "index.html"))

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "RideShare Web Application"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
