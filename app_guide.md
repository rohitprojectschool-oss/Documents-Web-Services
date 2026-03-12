# Crimson – E-Invoicing Platform (Backend Guide)

## Overview
This is the backend for Crimson, a multi-country e-invoicing platform. It is built using FastAPI and integrates with PostgreSQL and legacy SAP HANA DB.

## Tech Stack
- FastAPI (0.135.1)
- Pydantic V2
- SQLAlchemy (2.0.48)
- PostgreSQL (Primary DB)
- `sqlalchemy-hana` (Legacy Support)

## Directory Structure
- `backend/app/api/endpoints/`: REST API endpoints.
- `backend/app/schemas/`: Request/Response schemas.
- `backend/app/models/`: Database models.
- `backend/app/core/`: Core logic (auth, config).
- `backend/app/db/`: Database connection logic.

## Current State
- [x] Basic FastAPI app setup.
- [x] Route structure defined.
- [x] Core configuration with Pydantic Settings.
- [x] Database session management with SQLAlchemy and `get_db`.
- [x] Initial SQLAlchemy models for Customers and Invoices.
- [x] Binary storage for invoice attachments (stored as `BYTEA` in DB).
- [x] Absolute URL generation for attachments using `request.base_url`.
- [x] Path-based route matching (`:path`) to support IDs with slashes.
- [x] Filename sanitization to prevent UnicodeEncodeErrors in headers.
- [x] Deployment ready (Dockerfile + Render).
- [ ] Implement CRUD for Customers using real DB session.
- [ ] Migrate other endpoints (Analytics) to DB models.

## Deployment (Render)
- **Runtime:** Docker
- **Build Command:** Auto-detected from `Dockerfile`
- **Environment Variables:** `DATABASE_URL` (PostgreSQL), `SECRET_KEY`
- **Backend URL:** `https://documents-web-services.onrender.com`

## API Endpoints (Live)
- `/auth/me`: Current user profile.
- `/api/country-settings/public`: Public country settings.
- `/api/invoices`: [GET] List all / [POST] Upload new invoice.
- `/api/invoices/{doc_id:path}/file`: [GET] Fetch invoice attachment from DB.
- `/api/customers`: [GET] List all / [POST] Create new customer.
- `/api/analytics`: Stats and chart data.
- `/api/settings`: User/Account settings.
- `/health`: DB connection check.

## Environment Variables
- `DATABASE_URL`: Primary PostgreSQL connection string.
- `HANA_DB_HOST`, `HANA_DB_PORT`, `HANA_DB_USER`, `HANA_DB_PASSWORD`: (Optional) Legacy HANA support.
- `SECRET_KEY`: JWT/Session secret key.
