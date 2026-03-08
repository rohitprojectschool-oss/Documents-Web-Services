# AI Instructions for Crimson Backend

Follow these instructions when building the backend:

1.  **FastAPI Standards:** Use FastAPI's dependency injection system, Pydantic models for validation, and proper status codes. All route handlers should reside in `app/api/endpoints/`.
2.  **Modular Design:** Maintain strict separation of concerns:
    *   `app/models/`: Database schema definitions.
    *   `app/schemas/`: API payload validation and serialization.
    *   `app/api/endpoints/`: Routing and controller logic.
3.  **HANA DB Integration:** 
    *   Use SQLAlchemy with the `sqlalchemy-hana` dialect for all database interactions.
    *   **Always** use the `get_db` dependency (`Depends(get_db)`) to manage database sessions in route handlers to ensure proper connection lifecycle management.
    *   Leverage SQLAlchemy's ORM for CRUD operations and aggregations; avoid raw SQL strings where possible.
4.  **Data Flow (Model -> Schema):** Ensure raw data retrieved via SQLAlchemy `Models` is explicitly transformed and serialized using Pydantic `Schemas` before being returned to the frontend.
5.  **Error Handling:** Use FastAPI's `HTTPException` with appropriate status codes and detail messages for API errors. Log actual exceptions internally.
6.  **Documentation:** Keep the `app_guide` updated with all API changes, architectural decisions, and setup processes.
7.  **Security:** Ensure sensitive configuration (like HANA credentials) is loaded via `pydantic-settings` from environment variables, never hardcoded.
8.  **Async First:** Prefer `async def` for route handlers. When performing heavy synchronous DB operations, ensure they don't excessively block the event loop.
9.  **Pydantic V2:** Utilize Pydantic V2 features for accurate and efficient data validation.
