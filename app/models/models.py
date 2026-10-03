from datetime import datetime, timezone
from enum import Enum as PyEnum
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class GenderEnum(str, PyEnum):
    MALE = "MALE"
    FEMALE = "FEMALE"


class AppointmentStatus(str, PyEnum):
    AVAILABLE = "AVAILABLE"
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)

    reviews = relationship("Review", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    medical_council_code = Column(String(20), unique=True, nullable=False)  
    specialty = Column(String(100), nullable=False, index=True) 
    city = Column(String(50), nullable=False, index=True)  
    address = Column(Text, nullable=False)  
    experience_years = Column(Integer, default=0)  
    gender = Column(Enum(GenderEnum), nullable=False)

    about = Column(Text, nullable=True)  
    phone = Column(String(20), nullable=True)  
    instagram = Column(String(100), nullable=True)  
    website = Column(String(100), nullable=True)  

    rating = Column(Float, default=0.0)  
    reviews_count = Column(Integer, default=0)  

    has_online_visit = Column(Boolean, default=False)  
    has_in_person_visit = Column(Boolean, default=True)  

    reviews = relationship("Review", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")

    visit_price = Column(Integer, default=200000)  
    service_fee = Column(Integer, default=20000)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(
        Integer, ForeignKey("users.id"), nullable=True
    )   

    date_time = Column(DateTime, nullable=False, index=True)
    status = Column(
        Enum(AppointmentStatus), default=AppointmentStatus.AVAILABLE
    )

    patient_name = Column(String(100), nullable=True)
    patient_phone = Column(String(15), nullable=True)

    tracking_code = Column(
        String(20), unique=True, nullable=True, index=True
    )   
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("User", back_populates="appointments")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    rating = Column(Integer, nullable=False)  
    comment = Column(Text, nullable=True)  
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    doctor = relationship("Doctor", back_populates="reviews")
    patient = relationship("User", back_populates="reviews")