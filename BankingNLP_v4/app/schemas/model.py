from typing import Optional, Dict
from pydantic import BaseModel

class ModelRetrainRequest(BaseModel):
    triggered_by: str
    data_range: Optional[Dict[str, str]]
    model_type: Optional[str] = "llm"

class ModelRetrainResponse(BaseModel):
    status: str
    message: str 