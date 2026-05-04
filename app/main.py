

import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router, get_ranker


# ─── Lifespan: startup / shutdown ────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: warm up the ranker singleton
    print("[Startup] Initializing Resume Ranker...")
    get_ranker()
    print("[Startup] Ready.")
    yield
    # Shutdown
    print("[Shutdown] Cleaning up.")


# ─── App Factory ─────────────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title="Resume Screening API",
        description=(
            "AI-powered resume screening and ranking service.\n\n"
            "Uses **TF-IDF similarity**, **keyword overlap analysis**, "
            "and **section coverage scoring** to rank candidates against job descriptions.\n\n"
            "Supports single, batch, and file-upload workflows."
        ),
        version="1.0.0",
        contact={"name": "Resume Screener", "email": "api@resume-screener.ai"},
        license_info={"name": "MIT"},
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── CORS ──────────────────────────────────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Request Logging Middleware ────────────────────────────────────────────
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        req_id = str(uuid.uuid4())[:8]
        t0 = time.perf_counter()
        response = await call_next(request)
        elapsed = round((time.perf_counter() - t0) * 1000, 1)
        print(f"[{req_id}] {request.method} {request.url.path} → {response.status_code} ({elapsed}ms)")
        response.headers["X-Request-ID"] = req_id
        response.headers["X-Processing-Time-Ms"] = str(elapsed)
        return response

    # ── Global Exception Handler ─────────────────────────────────────────────
    @app.exception_handler(Exception)
    async def global_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "detail": str(exc), "code": 500},
        )

    # ── Routes ────────────────────────────────────────────────────────────────
    app.include_router(router, prefix="/api/v1")

    from app.api.classifier_routes import router as clf_router
    app.include_router(clf_router, prefix="/api/v1")

    @app.get("/", tags=["Root"])
    async def root():
        return {
            "service": "Resume Screening API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/v1/health",
        }

    return app


app = create_app()
