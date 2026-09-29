from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..models import BookingRequest
from ..schemas import BookingCreate, SubmissionResponse
from ..services.email_service import send_notification
from ..services.whatsapp_service import send_booking_notification

router = APIRouter(prefix="/api/bookings", tags=["bookings"])


def reference() -> str:
    return f"GV-{datetime.now(timezone.utc):%Y%m%d}-{datetime.now(timezone.utc).strftime('%H%M%S%f')[:8]}"


@router.post("", response_model=SubmissionResponse, status_code=201)
def create_booking(payload: BookingCreate, request: Request, db: Session = Depends(get_db)):
    settings = get_settings()
    ref = reference()
    booking = BookingRequest(reference_number=ref, **payload.model_dump())
    db.add(booking)
    db.commit()

    details = "\n".join(f"{key}: {value or '-'}" for key, value in payload.model_dump().items())
    details = f"Reference Number: {ref}\nSubmission Time: {datetime.now(timezone.utc).isoformat()}\n{details}"
    send_notification(settings, "New GV Diagnostics Test Booking", details)
    send_booking_notification(settings, ref, details)
    return SubmissionResponse(reference_number=ref, status=booking.status)
