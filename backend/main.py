import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import upload, predict, report

app = FastAPI(title="Dementia Detect API", version="1.0")

# Ensure static directory exists
os.makedirs("backend/static", exist_ok=True)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for generated heatmaps/reports
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Include routers
app.include_router(upload.router, prefix="/api", tags=["Upload"])
app.include_router(predict.router, prefix="/api", tags=["Predict"])
app.include_router(report.router, prefix="/api", tags=["Report"])

@app.get("/")
def read_root():
    return {"message": "Dementia Detect API is running."}
