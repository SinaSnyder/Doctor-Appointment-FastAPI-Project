from fastapi import FastAPI
from app.database import Base, engine
from app.models import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Doctor Appointment API")


@app.get("/")
def read_root():
    return {"message": "Doctor Appointment API is running!"}