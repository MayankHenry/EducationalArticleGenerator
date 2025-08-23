# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import generator

app = FastAPI(
    title="Educational Article Generator API",
    description="A simple API for generating educational articles.",
    version="1.0.0",
)

# CORS configuration
origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    # You can add more origins here, like a live website URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Include the API router
app.include_router(generator.router)

# Root endpoint for verification
@app.get("/")
def read_root():
    return {"message": "Welcome to the Educational Article Generator API!"}