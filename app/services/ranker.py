"""ResumerRanker singleton that attempts to load ML artefacts from disk.

This implementation is resilient: if `joblib` or model files are missing
it falls back to a lightweight scoring method so the API stays operational
for demos and testing.
"""
from __future__ import annotations

import json
from threading import Lock
from typing import Any, Dict, List, Optional
from pathlib import Path

from app.core.config import VECTORIZER_PATH, CLASSIFIER_PATH, CLASSIFIER_META_PATH

try:
    import joblib
except Exception:  # pragma: no cover - runtime environment may lack joblib
    joblib = None


class ResumerRanker:
    def __init__(self) -> None:
        self._loaded = False
        self.vectorizer: Optional[Any] = None
        self.classifier: Optional[Any] = None
        self.meta: Dict[str, Any] = {}

    def load(self) -> None:
        # Try to load vectorizer and classifier if available
        try:
            if joblib and Path(VECTORIZER_PATH).exists():
                self.vectorizer = joblib.load(VECTORIZER_PATH)
            if joblib and Path(CLASSIFIER_PATH).exists():
                self.classifier = joblib.load(CLASSIFIER_PATH)
            if Path(CLASSIFIER_META_PATH).exists():
                with open(CLASSIFIER_META_PATH, "r", encoding="utf8") as fh:
                    self.meta = json.load(fh)
            self._loaded = bool(self.vectorizer or self.classifier)
        except Exception:
            # Keep fallback behavior if loading fails
            self._loaded = False

    def health_check(self) -> Dict[str, Any]:
        return {
            "models_loaded": self._loaded,
            "vectorizer": bool(self.vectorizer),
            "classifier": bool(self.classifier),
            "meta_keys": list(self.meta.keys()),
        }

    def rank(self, job_description: str, resumes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # If TF-IDF vectorizer is available, score by cosine similarity where possible.
        if self.vectorizer is not None:
            try:
                from sklearn.metrics.pairwise import cosine_similarity
                jd_vec = self.vectorizer.transform([job_description])
                texts = [(r.get("text") or "") for r in resumes]
                doc_vecs = self.vectorizer.transform(texts)
                sims = cosine_similarity(jd_vec, doc_vecs).flatten().tolist()
                results = []
                for r, s in zip(resumes, sims):
                    results.append({"id": r.get("id"), "score": float(s)})
                return sorted(results, key=lambda x: x["score"], reverse=True)
            except Exception:
                # fall through to simple overlap scoring
                pass

        jd_tokens = set(job_description.lower().split())
        results: List[Dict[str, Any]] = []
        for i, r in enumerate(resumes):
            text = (r.get("text") or "").lower()
            overlap = len(jd_tokens.intersection(set(text.split())))
            results.append({"id": r.get("id", i), "score": float(overlap)})
        return sorted(results, key=lambda x: x["score"], reverse=True)

    def classify(self, text: str) -> Dict[str, Any]:
        if self.classifier is not None and self.vectorizer is not None:
            try:
                X = self.vectorizer.transform([text])
                if hasattr(self.classifier, "predict_proba"):
                    probs = self.classifier.predict_proba(X)[0]
                    idx = int(probs.argmax())
                    label = self.classifier.classes_[idx]
                    confidence = float(probs[idx])
                    return {"label": str(label), "confidence": confidence}
                else:
                    label = self.classifier.predict(X)[0]
                    return {"label": str(label), "confidence": 1.0}
            except Exception:
                pass
        return {"label": "unknown", "confidence": 0.0}


# Singleton management
_instance: Optional[ResumerRanker] = None
_lock = Lock()


def get_ranker() -> ResumerRanker:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = ResumerRanker()
                _instance.load()
    return _instance
