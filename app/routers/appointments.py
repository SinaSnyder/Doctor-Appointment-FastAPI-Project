from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Appointment, AppointmentStatus, Doctor
from app.schemas.schemas import (
    AppointmentResponse,
    BookAppointmentRequest,
)

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/book/{appointment_id}")
def book_appointment(
    payload: BookAppointmentRequest, db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == payload.appointment_id,
            Appointment.status == AppointmentStatus.AVAILABLE,
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Appointment slot is not available",
        )

    appointment.status = AppointmentStatus.BOOKED
    appointment.patient_name = payload.patient_name
    appointment.patient_phone = payload.patient_phone

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment reserved successfully",
        "appointment_id": appointment.id,
    }