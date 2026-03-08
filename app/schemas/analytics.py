from typing import List, Dict, Any
from pydantic import BaseModel

class CountryStat(BaseModel):
    countryCode: str
    countryName: str
    total: int
    accepted: int
    rejected: int
    pending: int

class MonthlyTrend(BaseModel):
    month: str
    AO: int = 0
    NG: int = 0
    PT: int = 0
    SA: int = 0

class DocTypeStat(BaseModel):
    type: str
    count: int
    color: str

class AnalyticsData(BaseModel):
    totalDocuments: int
    acceptanceRate: int
    rejectionRate: int
    activeCountries: int
    countryStats: List[CountryStat]
    monthlyTrends: List[MonthlyTrend]
    docTypeStats: List[DocTypeStat]

class AnalyticsResponse(BaseModel):
    status: bool
    data: AnalyticsData
