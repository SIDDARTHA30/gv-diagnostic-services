from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config import get_settings
from ..database import get_db
from ..models import ContactMessage
from ..schemas import ContactCreate, SubmissionResponse
from ..services.email_service import send_notification
from .bookings import reference

router = APIRouter(prefix="/api/contact", tags=["contact"])


@router.post("", response_model=SubmissionResponse, status_code=201)
def create_contact(payload: ContactCreate, db: Session = Depends(get_db)):
    settings = get_settings()
    ref = reference()
    message = ContactMessage(reference_number=ref, **payload.model_dump())
    db.add(message)
    db.commit()
    details = "\n".join(f"{key}: {value}" for key, value in payload.model_dump().items())
    details = f"Reference Number: {ref}\nSubmission Time: {datetime.now(timezone.utc).isoformat()}\n{details}"
    send_notification(settings, "New GV Diagnostics Contact Message", details)
    return SubmissionResponse(reference_number=ref, status=message.status)
