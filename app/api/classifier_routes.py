"""Classifier API routes (minimal)."""
from typing import Any, Dict

from fastapi import APIRouter

from app.services.ranker import get_ranker
from app.schemas.requests import ClassifyRequest, ClassifyResponse

router = APIRouter()


@router.post("/classify", response_model=ClassifyResponse, tags=["Classify"])
def classify(request: ClassifyRequest) -> ClassifyResponse:
    ranker = get_ranker()
    return ClassifyResponse(**ranker.classify(request.text))
