import logging
import time
from collections import defaultdict, deque

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import get_settings
from .database import Base, engine
from .routes.bookings import router as bookings_router
from .routes.contact import router as contact_router

logging.basicConfig(level=logging.INFO)
settings = get_settings()
app = FastAPI(title="GV Diagnostic Services API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(dict.fromkeys([
        settings.frontend_url,
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ])),
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

_requests: dict[str, deque[float]] = defaultdict(deque)


@app.middleware("http")
async def request_guard(request: Request, call_next):
    if request.method == "POST" and request.url.path in {"/api/bookings", "/api/contact"}:
        client = request.client.host if request.client else "unknown"
        now = time.monotonic()
        recent = _requests[client]
        while recent and now - recent[0] > 60:
            recent.popleft()
        if len(recent) >= settings.rate_limit_per_minute:
            return JSONResponse(status_code=429, content={"detail": "Too many requests. Please try again later."})
        recent.append(now)
        if request.headers.get("content-length") and int(request.headers["content-length"]) > 20000:
            return JSONResponse(status_code=413, content={"detail": "Request is too large."})
    return await call_next(request)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(bookings_router)
app.include_router(contact_router)
