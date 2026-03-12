from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db
from app.api.endpoints import auth, countries, invoices, customers, analytics, settings, users, dashboard

app = FastAPI(title="Crimson E-Invoicing Backend", version="1.0.0")

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

@app.get("/")
async def root():
    return {"message": "Crimson E-Invoicing Backend is running"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Check database connectivity."""
    try:
        # Simple query to check if database is responsive
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}
