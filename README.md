# personal-notes-manager-14197-14226

Notes Backend (FastAPI)

How to run (development):
1. cd notes_backend
2. Create a .env (or copy .env.example): cp .env.example .env
3. Install dependencies: pip install -r requirements.txt
4. Start server: uvicorn src.api.main:app --reload

Environment variables (see .env.example):
- DATABASE_URL: SQLAlchemy connection string (default sqlite:///./notes.db)
- DB_ECHO: true/false to echo SQL
- CORS_ALLOW_ORIGINS, CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS, CORS_ALLOW_CREDENTIALS
- API_TITLE, API_DESCRIPTION, API_VERSION

API
- GET    /              Health check
- GET    /notes         List notes
- POST   /notes         Create note
- GET    /notes/{id}    Get note
- PUT    /notes/{id}    Update note
- DELETE /notes/{id}    Delete note

OpenAPI docs available at /docs and /openapi.json
