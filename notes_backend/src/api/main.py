import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import init_db
from .routes import router as notes_router

# Load environment variables
load_dotenv()

API_TITLE = os.getenv("API_TITLE", "Notes API")
API_DESCRIPTION = os.getenv(
    "API_DESCRIPTION",
    "A FastAPI backend providing CRUD operations for personal notes.",
)
API_VERSION = os.getenv("API_VERSION", "1.0.0")

openapi_tags = [
    {"name": "Health", "description": "Service health and metadata endpoints."},
    {"name": "Notes", "description": "CRUD operations for managing notes."},
]

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    openapi_tags=openapi_tags,
)

# Configure CORS from .env, default to permissive for development
allow_origins_env = os.getenv("CORS_ALLOW_ORIGINS", "*")
allow_origins: List[str] = (
    [o.strip() for o in allow_origins_env.split(",")] if allow_origins_env != "*" else ["*"]
)
allow_methods = os.getenv("CORS_ALLOW_METHODS", "*")
allow_headers = os.getenv("CORS_ALLOW_HEADERS", "*")
allow_credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() in ("1", "true", "yes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=allow_methods if allow_methods != "*" else ["*"],
    allow_headers=allow_headers if allow_headers != "*" else ["*"],
)

# Initialize database and include routes
init_db()
app.include_router(notes_router)


@app.get("/", tags=["Health"], summary="Health Check", description="Simple health check endpoint.")
def health_check():
    """
    Health check endpoint.

    Returns:
    - 200 OK with a simple JSON indicating service is healthy.
    """
    return {"message": "Healthy"}
