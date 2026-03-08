from sqlalchemy import Column, String, Integer
from app.db.base_class import Base

class Country(Base):
    __tablename__ = "COUNTRIES"

    COUNTRY_CODE = Column(String(10), primary_key=True, index=True)
    COUNTRY_NAME = Column(String(100), nullable=False)
    FLAG_EMOJI = Column(String(10), nullable=True)
    DISPLAY_ORDER = Column(Integer, default=0)
    REGION = Column(String(50), nullable=True)
