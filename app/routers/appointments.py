from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.models import Appointment, AppointmentStatus, User
from app.schemas.schemas import AppointmentResponse, BookAppointmentRequest

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("/doctor/{doctor_id}", response_model=List[AppointmentResponse])
def get_doctor_available_appointments(
    doctor_id: int, db: Session = Depends(get_db)
):
    return (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.status == AppointmentStatus.AVAILABLE,
        )
        .all()
    )


@router.post("/book/{appointment_id}")
def book_appointment(
    appointment_id: int,
    payload: BookAppointmentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.id == appointment_id,
            Appointment.status == AppointmentStatus.AVAILABLE,
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This time slot is not available for booking or is already full",
        )

    appointment.status = AppointmentStatus.BOOKED
    appointment.user_id = current_user.id
    appointment.patient_name = payload.patient_name
    appointment.patient_phone = payload.patient_phone

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment successfully booked",
        "appointment_id": appointment.id,
    }


@router.get("/my-appointments", response_model=List[AppointmentResponse])
def get_my_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Appointment)
        .filter(Appointment.user_id == current_user.id)
        .all()
    )


@router.delete("/cancel/{appointment_id}")
def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.id == appointment_id)
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The desire Appointment was not found",
        )

    if appointment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to cancel other user's turns",
        )

    appointment.status = AppointmentStatus.AVAILABLE
    appointment.user_id = None
    appointment.patient_name = None
    appointment.patient_phone = None

    db.commit()

    return {"message": "Appointment successfully canceled"}