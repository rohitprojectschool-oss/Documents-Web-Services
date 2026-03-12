# AI Conventions for Crimson Backend

1.  **Naming Conventions:**
    *   Variables/Functions: `snake_case`
    *   Classes: `PascalCase`
    *   Constants: `UPPER_SNAKE_CASE`
    *   **Database Tables/Columns:** Use `UPPER_SNAKE_CASE` (e.g., `CUSTOMER_ID`, `DOC_STATUS`).
2.  **File Layout:**
    *   `app/api/endpoints/`: Route handlers.
    *   `app/schemas/`: Pydantic models (DTOs).
    *   `app/models/`: SQLAlchemy database entities.
    *   `app/core/`: Configuration, security, constants.
    *   `app/db/`: Session, base classes, setup/seed scripts.
3.  **API Response Structure:**
    *   Successful: `{"status": true, "data": ...}` or `{"success": true, "message": "...", "data": ...}`.
    *   Error: `{"status": false, "message": "...", "error": "..."}`.
4.  **Binary Content Handling:**
    *   Store as `LargeBinary` in SQLAlchemy models.
    *   Fetch only as needed in separate dedicated download/view endpoints.
    *   Use `urllib.parse.quote` for encoding path IDs that may contain spaces or slashes.
    *   **ALWAYS** use `filename*=UTF-8''` parameter in `Content-Disposition` for filenames.
5.  **Type Hinting:** Mandatory for all signatures and class members.
6.  **Logging & Debugging:** Use standard `logging` and avoid persistent `print` statements in production.
7.  **Database Management:**
    *   Use `app.db.setup_db` for initial table creation.
    *   PostgreSQL is primary; SAP HANA is legacy fallback.
8.  **Docstrings:** Google-style docstrings for all public components.
