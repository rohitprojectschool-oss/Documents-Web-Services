# AI Conventions for Crimson Backend

1.  **Naming Conventions:**
    *   Variables/Functions: `snake_case`
    *   Classes: `PascalCase`
    *   Constants: `UPPER_SNAKE_CASE`
    *   **Database Tables/Columns:** Use `UPPER_SNAKE_CASE` (e.g., `CUSTOMER_ID`, `DOC_STATUS`) to align strictly with SAP HANA standard conventions.
2.  **File Layout:**
    *   `app/api/endpoints/`: Route handlers.
    *   `app/schemas/`: Pydantic models for UI data contracts (DTOs).
    *   `app/models/`: SQLAlchemy models for database entities.
    *   `app/core/`: Configuration (`config.py`), security, and constants.
    *   `app/db/`: Database session (`session.py`), declarative base (`base_class.py`), and setup/seed scripts.
3.  **API Response Structure:**
    *   Successful: `{"status": true, "data": ...}` or `{"success": true, "message": "...", "data": ...}` to match established frontend contracts.
    *   Error: `{"status": false, "message": "...", "error": "..."}` or standard FastAPI JSON error responses.
4.  **Type Hinting:** Mandatory for all function signatures and class members to ensure static analysis and documentation accuracy.
5.  **Logging:** Use Python's standard `logging` module for operational insights and error tracking.
6.  **Database Management:**
    *   Use `app.db.setup_db` for initial table creation.
    *   Use `app.db.seed_db` for populating initial data.
7.  **Docstrings:** Use Google-style docstrings for all public functions and classes to clarify intent and usage.
