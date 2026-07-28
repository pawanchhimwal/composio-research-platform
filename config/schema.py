"""Pydantic schemas for data validation."""
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional, TypeVar, Generic
from config.constants import AuthMethod, ApiType, Buildability, VerificationState, SelfServeStatus

T = TypeVar('T')

class EvidenceDetail(BaseModel):
    url: HttpUrl
    reason: str

class VerifiedField(BaseModel, Generic[T]):
    value: T
    confidence: float = Field(..., ge=0.0, le=100.0)
    verified: bool
    evidence: Optional[EvidenceDetail] = None

class ApplicationEvidenceMap(BaseModel):
    authentication: Optional[EvidenceDetail] = None
    api_type: Optional[EvidenceDetail] = None
    self_serve: Optional[EvidenceDetail] = None
    buildability: Optional[EvidenceDetail] = None

class ApplicationIntelligence(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    category: str
    website: str
    description: str = ""
    authentication: List[AuthMethod]
    self_serve: SelfServeStatus
    developer_access: str = ""
    api_type: ApiType
    api_surface: str = ""
    api_breadth: str = ""
    mcp_support: bool = False
    buildability: Buildability
    blocker: Optional[str] = None
    evidence: ApplicationEvidenceMap
    confidence: float = Field(..., ge=0.0, le=100.0)
    verification_status: VerificationState = VerificationState.PENDING
    notes: str = ""

class VerifiedApplicationIntelligence(BaseModel):
    id: int
    name: str
    category: VerifiedField[str]
    description: VerifiedField[str]
    authentication: VerifiedField[List[AuthMethod]]
    self_serve: VerifiedField[SelfServeStatus]
    developer_access: VerifiedField[str]
    api_type: VerifiedField[ApiType]
    api_breadth: VerifiedField[str]
    mcp_support: VerifiedField[bool]
    buildability: VerifiedField[Buildability]
    blocker: VerifiedField[Optional[str]]
    overall_confidence: float = Field(..., ge=0.0, le=100.0)
    verification_status: VerificationState = VerificationState.PENDING
    notes: str = ""
