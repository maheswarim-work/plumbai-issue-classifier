from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class IssueSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IssueUrgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EMERGENCY = "emergency"

class IssueCategory(str, Enum):
    LEAK = "leak"
    CLOG = "clog"
    WATER_HEATER = "water_heater"
    FAUCET = "faucet"
    TOILET = "toilet"
    DRAIN = "drain"
    PIPE = "pipe"
    SEWER = "sewer"
    GARBAGE_DISPOSAL = "garbage_disposal"
    WATER_PRESSURE = "water_pressure"
    OTHER = "other"

class IssueRequest(BaseModel):
    description: str = Field(..., min_length=10, max_length=1000, description="Customer's description of the plumbing issue")
    customer_name: Optional[str] = Field(None, max_length=100, description="Customer's name")
    phone_number: Optional[str] = Field(None, max_length=20, description="Customer's phone number")
    address: Optional[str] = Field(None, max_length=200, description="Service address")

class IssueClassification(BaseModel):
    category: IssueCategory
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: IssueSeverity
    urgency: IssueUrgency
    estimated_duration: str = Field(..., description="Estimated time to resolve")
    required_tools: List[str] = Field(..., description="Tools likely needed")
    recommended_parts: List[str] = Field(..., description="Parts that might be needed")
    safety_notes: List[str] = Field(..., description="Safety considerations")
    next_steps: List[str] = Field(..., description="Recommended next steps")

class IssueResponse(BaseModel):
    request_id: str
    classification: IssueClassification
    processing_time_ms: float
    model_version: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str
    uptime_seconds: float

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None 