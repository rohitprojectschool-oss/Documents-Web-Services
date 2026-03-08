from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth, countries, invoices, customers, analytics, settings, users, dashboard

app = FastAPI(title="Crimson E-Invoicing Backend", version="1.0.0")

# CORS Configuration
# In a real app, this should be more restrictive
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
