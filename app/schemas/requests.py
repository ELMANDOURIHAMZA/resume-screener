"""Pydantic request/response models (minimal)."""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

from app.core.config import DEFAULT_TOP_K


class Resume(BaseModel):
    id: Optional[str]
    text: str


class RankRequest(BaseModel):
    job_description: str
    resumes: List[Resume] = Field(default_factory=list)
    top_k: Optional[int] = None


class ResumeOut(BaseModel):
    resume_id: Optional[str]
    score: float
    category: Optional[str] = None
    confidence: Optional[float] = None
    keywords_matched: Optional[List[str]] = None


class RankResponse(BaseModel):
    results: List[ResumeOut]


class ClassifyRequest(BaseModel):
    text: str


class ClassifyResponse(BaseModel):
    label: str
    confidence: float
