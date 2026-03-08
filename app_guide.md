# Crimson – E-Invoicing Platform (Backend Guide)

## Overview
This is the backend for Crimson, a multi-country e-invoicing platform. It is built using FastAPI and will eventually integrate with SAP HANA DB.

## Tech Stack
- FastAPI
- Pydantic V2
- SQLAlchemy (with `sqlalchemy-hana`)
- SAP HANA Client (`hdbcli`)

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
- [x] Database session management with SQLAlchemy and `get_db` dependency.
- [x] Declarative base and naming conventions for SAP HANA (UPPER_SNAKE_CASE).
- [x] Initial SQLAlchemy model for Customers.
- [x] Deployment ready (Dockerfile + Render).
- [ ] Implement CRUD for Customers using real DB session.
- [ ] Migrate other endpoints (Invoices, Analytics) to DB models.
- [ ] SAP HANA DB connection validation.

## Deployment (Render)
- **Runtime:** Docker
- **Build Command:** Auto-detected from `Dockerfile`
- **Environment Variables:** `HANA_DB_HOST`, `HANA_DB_PORT`, `HANA_DB_USER`, `HANA_DB_PASSWORD`, `HANA_DB_SCHEMA`
- **Backend URL:** `https://documents-web-services.onrender.com`

## API Endpoints (Live)
- `/auth/me`: Current user profile.
- `/api/country-settings/public`: Public country settings.
- `/api/invoices`: [GET] List all / [POST] Upload new invoice.
- `/api/customers`: [GET] List all / [POST] Create new customer.
- `/api/analytics`: Stats and chart data.
- `/api/settings`: User/Account settings.
- `/health`: DB connection check.

## Environment Variables
- `HANA_DB_HOST`: SAP HANA host.
- `HANA_DB_PORT`: SAP HANA port.
- `HANA_DB_USER`: SAP HANA user.
- `HANA_DB_PASSWORD`: SAP HANA password.
- `SECRET_KEY`: JWT/Session secret key.
