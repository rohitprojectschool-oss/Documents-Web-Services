from typing import List, Optional
from pydantic import BaseModel

class Country(BaseModel):
    country_code: str
    country_name: str
    flag_emoji: Optional[str] = None
    display_order: int
    region: Optional[str] = None

class CountrySettingsData(BaseModel):
    countries: List[Country]
    sort_mode: str
    use_only_configured: bool
    show_empty_countries: bool

class CountrySettingsResponse(BaseModel):
    status: bool
    data: CountrySettingsData
