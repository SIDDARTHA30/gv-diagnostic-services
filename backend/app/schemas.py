from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, model_validator


def clean_text(value: str, max_length: int) -> str:
    cleaned = " ".join(value.strip().split())
    if not cleaned:
        raise ValueError("This field is required.")
    return cleaned[:max_length]


class BookingCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=7, max_length=32)
    email: EmailStr | None = None
    test: str = Field(min_length=2, max_length=160)
    collection_type: Literal["Centre Visit", "Home Sample Pickup"]
    preferred_date: date | None = None
    preferred_time: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=300)
    city: str | None = Field(default=None, max_length=100)
    notes: str | None = Field(default=None, max_length=2000)

    @field_validator("name", "test", "phone")
    @classmethod
    def normalize_required_text(cls, value: str) -> str:
        return clean_text(value, 2000)

    @field_validator("address", "city", "preferred_time", "notes")
    @classmethod
    def normalize_optional_text(cls, value: str | None) -> str | None:
        return clean_text(value, 2000) if value else None

    @model_validator(mode="after")
    def require_pickup_address(self):
        if self.collection_type == "Home Sample Pickup" and not self.address:
            raise ValueError("Address is required for home sample pickup.")
        return self


class ContactCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=7, max_length=32)
    email: EmailStr
    subject: str = Field(min_length=2, max_length=160)
    message: str = Field(min_length=2, max_length=3000)

    @field_validator("name", "phone", "subject", "message")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        return clean_text(value, 3000)


class SubmissionResponse(BaseModel):
    reference_number: str
    status: str
