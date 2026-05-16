"""Main API routes (minimal implementation).

Provides /health and /rank endpoints and exposes get_ranker() to initialize
or fetch the singleton ranker instance.
"""
from typing import Any, Dict, List

from fastapi import APIRouter

from app.services.ranker import get_ranker
from app.schemas.requests import RankRequest, RankResponse, ResumeOut
from app.core.config import DEFAULT_TOP_K, MAX_TOP_K

router = APIRouter()


@router.get("/health", tags=["Health"])
def health() -> Dict[str, Any]:
    ranker = get_ranker()
    return {"status": "ok", "details": ranker.health_check()}


@router.post("/rank", response_model=RankResponse, tags=["Rank"])
def rank(request: RankRequest) -> RankResponse:
    """Rank resumes against a job description and return top-k results.
    """
    ranker = get_ranker()
    jd = request.job_description
    resumes = [r.dict() for r in (request.resumes or [])]
    # If frontend does not provide resumes, fallback to dataset (data/Resume.csv)
    if not resumes:
        try:
            import pandas as _pd
            from app.core.config import RESUME_CSV
            df = _pd.read_csv(RESUME_CSV)
            # expect column Resume_str
            resumes = [{"id": str(i), "text": str(t)} for i, t in enumerate(df['Resume_str'].astype(str).tolist())]
        except Exception:
            resumes = []
    raw = ranker.rank(jd, resumes)

    # enrich results with classification where available
    enriched: List[ResumeOut] = []
    for item in raw:
        # find resume text by id
        rid = item.get("id")
        matched = None
        for r in resumes:
            if str(r.get("id")) == str(rid) or (rid is None and r.get("text") == r.get("text")):
                matched = r
                break
        category = None
        confidence = None
        if matched:
            cls = ranker.classify(matched.get("text", ""))
            category = cls.get("label")
            confidence = float(cls.get("confidence", 0.0))
        keywords = []
        enriched.append(ResumeOut(resume_id=str(rid) if rid is not None else None, score=float(item.get("score", 0.0)), category=category, confidence=confidence, keywords_matched=keywords))

    # apply top_k
    top_k = request.top_k or DEFAULT_TOP_K
    top_k = max(1, min(int(top_k), MAX_TOP_K))
    return RankResponse(results=enriched[:top_k])
