from typing import List, Optional
from pydantic import BaseModel

class StatsSummary(BaseModel):
    totalDocuments: int
    pending: int
    completed: int
    rejected: int

class ActivityPoint(BaseModel):
    date: str
    count: int

class CountryShare(BaseModel):
    name: str
    value: int
    color: str

class DocTypeShare(BaseModel):
    type: str
    percentage: int
    color: str

class RecentDocument(BaseModel):
    docId: str
    sourceReference: str
    customer: str
    grossAmount: str
    created: str
    status: str
    docType: str
    hasAttachment: bool
    fileUrl: Optional[str] = None

class DashboardData(BaseModel):
    stats: StatsSummary
    activityData: List[ActivityPoint]
    countryData: List[CountryShare]
    docDistribution: List[DocTypeShare]
    recentDocuments: List[RecentDocument]

class DashboardResponse(BaseModel):
    status: bool
    data: DashboardData
