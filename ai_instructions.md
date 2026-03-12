# AI Instructions for Crimson Backend

Follow these instructions when building the backend:

1.  **FastAPI Standards:** Use FastAPI's dependency injection system, Pydantic models for validation, and proper status codes. All route handlers should reside in `app/api/endpoints/`.
2.  **Modular Design:** Maintain strict separation of concerns:
    *   `app/models/`: Database schema definitions.
    *   `app/schemas/`: API payload validation and serialization.
    *   `app/api/endpoints/`: Routing and controller logic.
3.  **Database Integration (PostgreSQL/HANA):** 
    *   Use SQLAlchemy for all database interactions.
    *   **Always** use the `get_db` dependency (`Depends(get_db)`) to manage database sessions.
4.  **Binary File Storage:**
    *   Store invoice attachments as binary data in the database using the `LargeBinary` column type (`BYTEA` in PostgreSQL).
    *   Always store accompanying metadata: `FILE_NAME`, `FILE_MIME_TYPE`.
    *   Serve files via a dedicated endpoint using `Response(content=inv.FILE_CONTENT, ...)` to avoid loading issues with large objects.
5.  **URL Generation & Routing:**
    *   Generate **absolute URLs** for file attachments using `request.base_url` to ensure compatibility with frontends on different ports/domains.
    *   Use query parameters (e.g. `?docId=...`) for IDs that may contain slashes. Avoid path-based routing (e.g. `/{doc_id:path}`) for these IDs, as reverse proxies, frameworks, and browsers often struggle with double-encoded or raw slashes in the path.
6.  **Performance Optimization:**
    *   **CRITICAL:** When querying lists from the database (e.g. `get_invoices`, `get_dashboard` recent docs), ensure you **exclude** `LargeBinary` columns. You can do this by using explicit `select(...)` statements for the exact fields needed, or by using `sqlalchemy.orm.defer(Model.BINARY_COLUMN)`. Failure to do this will result in severe API lag due to transmitting massive binary blobs across the network for every row in a list.
    *   Consolidate `.count()` queries where possible.
7.  **HTTP Header Safety:**
    *   Sanitize filenames in `Content-Disposition` headers to avoid `UnicodeEncodeError`. 
    *   Always provide an ASCII-only `filename="..."` and a UTF-8 encoded `filename*=UTF-8''..."`.
8.  **Data Flow (Model -> Schema):** Ensure raw data retrieved via SQLAlchemy `Models` is explicitly transformed and serialized using Pydantic `Schemas`.
9.  **Error Handling:** Use FastAPI's `HTTPException` with appropriate status codes.
10. **Async First:** Prefer `async def` for route handlers.
11. **Pydantic V2:** Utilize Pydantic V2 features for accurate validation.
