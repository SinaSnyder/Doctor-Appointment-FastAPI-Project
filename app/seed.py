from datetime import datetime, timedelta
from app.database import SessionLocal, engine, Base
from app.models.models import Doctor, Appointment, AppointmentStatus, GenderEnum

Base.metadata.create_all(bind=engine)


def seed_data():
    db = SessionLocal()
    if db.query(Doctor).first():
        print("Initial data has already been added")
        db.close()
        return

    doc1 = Doctor(
        full_name="Doctor mmd qoli",
        specialty="Dentist",
        medical_council_code="MC-12345",
        city="Tehran",
        address="Tehran, velenjak",
        gender=GenderEnum.MALE,
        visit_price=250000,
        service_fee=25000,
    )
    db.add(doc1)
    db.commit()
    db.refresh(doc1)

    now = datetime.now()
    app1 = Appointment(
        doctor_id=doc1.id,
        date_time=now + timedelta(days=1, hours=2),
        status=AppointmentStatus.AVAILABLE,
    )
    app2 = Appointment(
        doctor_id=doc1.id,
        date_time=now + timedelta(days=1, hours=4),
        status=AppointmentStatus.AVAILABLE,
    )

    db.add_all([app1, app2])
    db.commit()
    db.close()
    print("Initial data was successfully cearted")


if __name__ == "__main__":
    seed_data()