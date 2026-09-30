from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from app.models.models import AppointmentStatus, GenderEnum


class UserBase(BaseModel):
    full_name: str
    phone_number: str = Field(..., pattern=r"^09\d{9}$")  


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class DoctorBase(BaseModel):
    full_name: str
    medical_council_code: str
    specialty: str
    city: str
    address: str
    experience_years: int = 0
    gender: GenderEnum
    about: Optional[str] = None
    phone: Optional[str] = None
    instagram: Optional[str] = None
    website: Optional[str] = None
    has_online_visit: bool = False
    has_in_person_visit: bool = True


class DoctorCreate(DoctorBase):
    pass


class DoctorResponse(DoctorBase):
    id: int
    rating: float
    reviews_count: int
    model_config = ConfigDict(from_attributes=True)


class ReviewCreate(BaseModel):
    doctor_id: int
    rating: int = Field(..., ge=1, le=5)   
    comment: Optional[str] = None


class ReviewResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AppointmentCreate(BaseModel):
    doctor_id: int
    date_time: datetime


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: Optional[int]
    date_time: datetime
    status: AppointmentStatus
    model_config = ConfigDict(from_attributes=True)


class BookAppointmentRequest(BaseModel):
    appointment_id: int
    patient_name: str
    patient_phone: str = Field(..., pattern=r"^09\d{9}$")


class AppointmentDetailResponse(BaseModel):
    id: int
    doctor_name: str
    specialty: str
    medical_council_code: str
    address: str
    date_time: datetime
    visit_price: int
    service_fee: int
    total_price: int