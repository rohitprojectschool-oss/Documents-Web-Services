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
    *   **CRITICAL:** When querying lists of objects containing `LargeBinary` columns, ALWAYS use `sqlalchemy.orm.defer(Model.FILE_CONTENT)` or explicit `select(...)` to exclude the heavy binary data, otherwise list endpoints will be extremely slow.
    *   Fetch only as needed in separate dedicated download/view endpoints.
    *   Use query parameters (e.g. `?docId=...`) instead of path parameters (`/{docId}`) when IDs can contain slashes, as path-based routing is prone to proxy/browser bugs with double-encoded slashes.
    *   **ALWAYS** use `filename*=UTF-8''` parameter in `Content-Disposition` for filenames.
5.  **Type Hinting:** Mandatory for all signatures and class members.
6.  **Logging & Debugging:** Use standard `logging` and avoid persistent `print` statements in production.
7.  **Database Management:**
    *   Use `app.db.setup_db` for initial table creation.
    *   PostgreSQL is primary; SAP HANA is legacy fallback.
8.  **Docstrings:** Google-style docstrings for all public components.
