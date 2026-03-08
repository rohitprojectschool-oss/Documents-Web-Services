from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    """Base class for all SQLAlchemy models."""
    id: any
    __name__: str

    # Automatically generate __tablename__ based on the class name
    # Using UPPER_SNAKE_CASE as per HANA conventions
    @declared_attr
    def __tablename__(cls) -> str:
        # Example: Customer -> CUSTOMER
        import re
        name = cls.__name__
        # Convert CamelCase to snake_case and then to upper case
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).upper()
        return name
