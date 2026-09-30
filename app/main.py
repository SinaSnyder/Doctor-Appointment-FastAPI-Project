from fastapi import FastAPI
from app.database import Base, engine
from app.routers import appointments, doctors

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Doctor Appointment API")

app.include_router(doctors.router)
app.include_router(appointments.router)


@app.get("/")
def read_root():
    return {"message": "Doctor Appointment API is running!"}