from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.api.endpoints import auth, countries, invoices, customers, analytics, settings, users, dashboard
import os

app = FastAPI(title="Crimson E-Invoicing Backend", version="1.0.0")

# Add Gzip Compression for large responses
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS Configuration
# When allow_credentials=True, allow_origins cannot be ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://documents-web-ui.vercel.app",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
)

# API Routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(countries.router, prefix="/api/country-settings", tags=["countries"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["invoices"])
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(settings.router, prefix="/api/settings", tags=["settings"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Check database connectivity."""
    try:
        # Simple query to check if database is responsive
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

# Serve static files from the frontend/dist directory if it exists
# In Docker, it's moved to /app/dist
frontend_path = "/app/dist"
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

    # Catch-all route to serve index.html for client-side routing
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/")
async def root():
    if os.path.exists(frontend_path):
        return FileResponse(os.path.join(frontend_path, "index.html"))
    return {"message": "Crimson E-Invoicing Backend is running"}
