from typing import Dict, Any, Optional
from pydantic import BaseModel

class CRMPushResultsRequest(BaseModel):
    conversation_id: str
    results: Dict[str, Any]
    crm_endpoint: Optional[str]

class CRMPushResultsResponse(BaseModel):
    status: str
    crm_response: Optional[str] 