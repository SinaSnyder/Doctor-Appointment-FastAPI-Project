# 🩺 Doctor Appointment Booking System

A production-oriented RESTful backend for managing **doctor availability, patient appointments, authentication, and secure booking workflows**.

Built with **FastAPI**, **SQLAlchemy**, **Alembic**, and **JWT-based authentication** with strict ownership checks for appointment operations.

---

## ✨ Features

### 🔐 Authentication & Authorization

- User registration and login (phone number + password)
- JWT access-token authentication (HS256)
- OAuth2 password flow (form-data login)
- Secure password hashing with `passlib` + bcrypt
- Protected user profile endpoint (`/auth/me`)
- Ownership-based authorization for appointment operations
- `403 Forbidden` for unauthorized appointment modifications

### 👨‍⚕️ Doctor Directory

- List doctors with filters: specialty, city, gender
- View detailed doctor profile
- Each doctor has: specialty, city, address, experience, gender, contact info, social links, rating, visit prices

### 📅 Appointment Management

- View available appointment slots for a doctor
- Book an available appointment (requires auth)
- View authenticated user's appointments
- Cancel owned appointments (reverts slot to AVAILABLE)
- Prevent unauthorized users from modifying other patients' appointments
- Appointment statuses: `AVAILABLE`, `BOOKED`, `CANCELLED`

### ⭐ Reviews

- Patients can create reviews for doctors (1-5 rating + optional comment)
- Reviews linked to doctor and patient
- Doctor rating and review count aggregated

### 🗄️ Database & Migrations

- SQLAlchemy ORM with declarative models
- Alembic for database migrations
- Seed script for initial doctors and appointment slots
- Uses **SQLite** for development, **PostgreSQL** for production (via `.env`)

### 📚 API Documentation

FastAPI auto-generates interactive docs:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend Framework | FastAPI |
| Language | Python 3.10+ |
| Database (dev) | SQLite |
| Database (prod) | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) + OAuth2 |
| Password Hashing | Passlib / bcrypt |
| ASGI Server | Uvicorn |
| Config | python-dotenv |

---

## 🏗️ Architecture

```
Client
  │
  ▼
FastAPI Application
  │
  ├── Routers
  │     ├── /auth        → Authentication endpoints
  │     ├── /doctors     → Doctor directory & profiles
  │     └── /appointments→ Booking, cancellation, listings
  │
  ├── Schemas (Pydantic) → Request/response validation
  ├── Models (SQLAlchemy)→ ORM models
  ├── Core
  │     ├── security.py  → JWT, password hashing
  │     └── config.py    → Settings from .env
  ├── deps.py            → Auth dependency (get_current_user)
  └── database.py        → Engine, session, Base
        │
        ▼
   SQLite / PostgreSQL
```

---

## 📁 Project Structure

```
.
├── app/
│   ├── core/
│   │   ├── config.py      # Settings from .env
│   │   └── security.py    # JWT + bcrypt utilities
│   │
│   ├── models/
│   │   └── models.py      # User, Doctor, Appointment, Review
│   │
│   ├── schemas/
│   │   └── schemas.py     # Pydantic request/response models
│   │
│   ├── routers/
│   │   ├── auth.py        # POST /register, /login, GET /me
│   │   ├── doctors.py     # GET /, /{id} with filters
│   │   └── appointments.py# GET/POST/DELETE appointment ops
│   │
│   ├── database.py        # SQLAlchemy engine + session
│   ├── deps.py            # get_current_user dependency
│   ├── main.py            # FastAPI app + router registration
│   └── seed.py            # Dev data seeding
│
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/          # Migration files (run alembic revision)
│
├── .env                   # Local config (not committed)
├── .env.example           # Template
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## 🗃️ Database Schema

### Models

**User** (`users` table)
| Column | Type | Constraints |
|---|---|---|
| id | Integer | PK, index |
| full_name | String(100) | NOT NULL |
| phone_number | String(15) | UNIQUE, index, NOT NULL |
| is_active | Boolean | DEFAULT true |
| hashed_password | String | |

**Doctor** (`doctors` table)
| Column | Type | Constraints |
|---|---|---|
| id | Integer | PK, index |
| full_name | String(100) | NOT NULL |
| medical_council_code | String(20) | UNIQUE, NOT NULL |
| specialty | String(100) | NOT NULL, index |
| city | String(50) | NOT NULL, index |
| address | Text | NOT NULL |
| experience_years | Integer | DEFAULT 0 |
| gender | Enum(GenderEnum) | NOT NULL |
| about | Text | NULLABLE |
| phone | String(20) | NULLABLE |
| instagram | String(100) | NULLABLE |
| website | String(100) | NULLABLE |
| rating | Float | DEFAULT 0.0 |
| reviews_count | Integer | DEFAULT 0 |
| has_online_visit | Boolean | DEFAULT false |
| has_in_person_visit | Boolean | DEFAULT true |
| visit_price | Integer | DEFAULT 200000 |
| service_fee | Integer | DEFAULT 20000 |

**Appointment** (`appointments` table)
| Column | Type | Constraints |
|---|---|---|
| id | Integer | PK, index |
| doctor_id | Integer | FK → doctors.id, NOT NULL |
| patient_id | Integer | FK → users.id, NULLABLE |
| date_time | DateTime | NOT NULL, index |
| status | Enum(AppointmentStatus) | DEFAULT AVAILABLE |
| patient_name | String(100) | NULLABLE |
| patient_phone | String(15) | NULLABLE |
| tracking_code | String(20) | UNIQUE, index, NULLABLE |
| created_at | DateTime | DEFAULT utcnow |
| updated_at | DateTime | DEFAULT utcnow, onupdate |

**Review** (`reviews` table)
| Column | Type | Constraints |
|---|---|---|
| id | Integer | PK, index |
| doctor_id | Integer | FK → doctors.id, NOT NULL |
| patient_id | Integer | FK → users.id, NOT NULL |
| rating | Integer | NOT NULL (1-5) |
| comment | Text | NULLABLE |
| created_at | DateTime | DEFAULT utcnow |

### Relationships

- **User** ↔ **Appointment**: One-to-Many (patient)
- **Doctor** ↔ **Appointment**: One-to-Many
- **User** ↔ **Review**: One-to-Many (patient)
- **Doctor** ↔ **Review**: One-to-Many

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git
- pip

---

### 1. Clone the Repository

```bash
git clone https://github.com/SinaSnyder/Doctor-Appointment-FastAPI-Project
cd doctor-appointment-fastapi
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / macOS
```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create a `.env` file in the project root (copy from `.env.example`):

```env
# JWT
SECRET_KEY=your_super_secret_jwt_key_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (SQLite for dev, PostgreSQL for prod)
# SQLite (default, no setup required):
DATABASE_URL=sqlite:///./doctor_appointment.db

# PostgreSQL (production):
# DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/dbname
```

> **Note**: The app defaults to SQLite (`doctor_appointment.db`) for zero-config development. Switch to PostgreSQL by setting `DATABASE_URL` in `.env`.

---

## 🗄️ Database Setup

### Run Migrations (PostgreSQL)

```bash
alembic upgrade head
```

### Create New Migration (after model changes)

```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

### Seed Initial Data

Populates doctors and appointment slots:

```bash
python -m app.seed
```

---

## ▶️ Running the Application

```bash
uvicorn app.main:app --reload
```

API available at: **`http://127.0.0.1:8000`**

---

## 🔑 Authentication Flow

```
Client
  │
  ├─ POST /auth/register  (JSON: full_name, phone_number, password)
  │
  ├─ POST /auth/login     (Form: username=phone_number, password)
  │        │
  │        └─ Returns: { "access_token": "...", "token_type": "bearer" }
  │
  ▼
Protected Endpoints
  │
  └─ Header: Authorization: Bearer <access_token>
```

### Register
```http
POST /auth/register
Content-Type: application/json

{
  "full_name": "John Doe",
  "phone_number": "09123456789",
  "password": "securepass123"
}
```

### Login (OAuth2 form-data)
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=09123456789&password=securepass123
```

### Get Profile
```http
GET /auth/me
Authorization: Bearer <access_token>
```

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/auth/register` | Register new user | ❌ |
| `POST` | `/auth/login` | Login, returns JWT | ❌ |
| `GET` | `/auth/me` | Get current user profile | ✅ |

### Doctors

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/doctors` | List doctors (filters: specialty, city, gender) | ❌ |
| `GET` | `/doctors/{doctor_id}` | Get doctor profile | ❌ |

### Appointments

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `GET` | `/appointments/doctor/{doctor_id}` | Available slots for doctor | ❌ |
| `POST` | `/appointments/book/{appointment_id}` | Book appointment | ✅ |
| `GET` | `/appointments/my-appointments` | Current user's appointments | ✅ |
| `DELETE` | `/appointments/cancel/{appointment_id}` | Cancel owned appointment | ✅ |

### Reviews

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| `POST` | `/reviews` | Create review | ✅ |
| `GET` | `/reviews/doctor/{doctor_id}` | Get doctor's reviews | ❌ |

> ✅ = Requires `Authorization: Bearer <token>` header

---

## 🧪 Testing with Swagger UI

1. Open `http://127.0.0.1:8000/docs`
2. **Register**: `POST /auth/register` → JSON body
3. **Login**: `POST /auth/login` → form-data (`username`=phone, `password`)
4. **Authorize**: Click 🔒 **Authorize** button, paste `access_token`
5. **Test protected endpoints**: Book, list, cancel appointments

---

## 🔒 Security & Access Control

- **JWT tokens** expire in 30 min (configurable)
- **Passwords** hashed with bcrypt (cost factor auto)
- **Appointment ownership**: Users can only cancel their own bookings
  - Attempting to cancel another user's appointment → `403 Forbidden`
- **Phone number** unique per user (used as login identifier)

---

## 🧩 Development Commands

| Command | Description |
|---|---|
| `uvicorn app.main:app --reload` | Start dev server |
| `alembic upgrade head` | Apply all migrations |
| `alembic revision --autogenerate -m "msg"` | Create migration |
| `alembic current` | Show current migration |
| `python seed.py` | Seed dev data |
| `pip install -r requirements.txt` | Install deps |

---

## 📌 Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SECRET_KEY` | Yes | — | JWT signing secret |
| `ALGORITHM` | No | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | Token TTL |
| `DATABASE_URL` | No | `sqlite:///./doctor_appointment.db` | DB connection string |

---

## 🚧 Roadmap / Future Improvements

- [ ] Doctor authentication & dashboard
- [ ] Admin role & management endpoints
- [ ] Doctor availability management (CRUD slots)
- [ ] Appointment rescheduling
- [ ] Email/SMS notifications
- [ ] Pagination & advanced search for doctors
- [ ] Rate limiting & API throttling
- [ ] Docker + Docker Compose
- [ ] Unit/integration tests (pytest + httpx)
- [ ] CI/CD pipeline
- [ ] Refresh token support
- [ ] Role-based access control (RBAC)
- [ ] API versioning

---

## 👨‍💻 Author

**Mohammad Sina Rahimi**  
GitHub: [@SinaSnyder](https://github.com/SinaSnyder)

---

## ⭐ Summary

**Doctor Appointment Booking System** demonstrates:

- REST API design with FastAPI
- JWT authentication + OAuth2 password flow
- SQLAlchemy 2.0 ORM with relationships
- Alembic migrations
- Pydantic v2 validation
- Ownership-based access control
- Modular project structure
- Auto-generated API documentation
- Zero-config dev setup (SQLite)
