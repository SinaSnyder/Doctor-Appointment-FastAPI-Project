from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Doctor
from app.schemas.schemas import DoctorResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get("/", response_model=List[DoctorResponse])
def get_doctors(
    specialty: Optional[str] = None,
    city: Optional[str] = None,
    gender: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Doctor)
    if specialty:
        query = query.filter(Doctor.specialty == specialty)
    if city:
        query = query.filter(Doctor.city == city)
    if gender:
        query = query.filter(Doctor.gender == gender)
    return query.all()


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor_profile(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found"
        )
    return doctor