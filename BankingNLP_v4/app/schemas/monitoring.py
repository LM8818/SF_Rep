from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class AlertGetQuery(BaseModel):
    level: Optional[str]
    since: Optional[str]

class AlertItem(BaseModel):
    id: str
    event: str
    level: str
    timestamp: str
    details: Optional[Dict[str, Any]]

class AlertResponse(BaseModel):
    alerts: List[AlertItem]

class AlertCreateRequest(BaseModel):
    event: str
    details: Optional[Dict[str, Any]] 