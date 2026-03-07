from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Explanation(BaseModel):
    heatmap_base64: str
    suspicious_frames: List[int]

class AnalyzeResponse(BaseModel):
    success: bool
    confidence: Optional[float] = None
    label: Optional[str] = None
    explanation: Optional[Explanation] = None
    error: Optional[str] = None

class ScanHistoryItem(BaseModel):
    scan_id: str
    filename: str
    confidence: float
    result_label: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

class ScanDetailItem(ScanHistoryItem):
    explanation_json: str
