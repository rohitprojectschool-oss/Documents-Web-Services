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
    *   Use path-based routing for IDs that may contain slashes (e.g., `@router.get("/{doc_id:path}/file")`).
    *   When generating URLs for paths with slashes, use `quote(id, safe='/')` to ensure spaces are encoded but slashes remain literal for the `:path` match.
6.  **HTTP Header Safety:**
    *   Sanitize filenames in `Content-Disposition` headers to avoid `UnicodeEncodeError`. 
    *   Always provide an ASCII-only `filename="..."` and a UTF-8 encoded `filename*=UTF-8''..."`.
7.  **Data Flow (Model -> Schema):** Ensure raw data retrieved via SQLAlchemy `Models` is explicitly transformed and serialized using Pydantic `Schemas`.
8.  **Error Handling:** Use FastAPI's `HTTPException` with appropriate status codes.
9.  **Async First:** Prefer `async def` for route handlers.
10. **Pydantic V2:** Utilize Pydantic V2 features for accurate validation.
