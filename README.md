# Job Application Tracker

A secure REST API for managing job applications, tracking recruitment stages, and analyzing job search progress.

## 🚀 Features

### 🔐 Authentication & Authorization

- User registration and login
- JWT-based authentication
- Password hashing
- Protected API endpoints
- User-specific application ownership
- Users cannot access or modify another user's applications

### 📋 Application Management

- Create job applications
- View active applications
- View individual applications
- Update application details
- Archive applications
- Permanently delete applications
- Filter applications by recruitment status
- Sort applications by application date

### 📊 Analytics

- Total applications
- Applications grouped by status
- Applications grouped by company
- Interview conversion rate
- Archived applications are retained in analytics

### 🧪 Testing

- Automated API testing using `pytest`
- FastAPI `TestClient`
- Authentication and authorization testing
- Application CRUD testing
- Archive behavior testing
- User ownership/security testing

## 🛠️ Tech Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- JWT
- Alembic
- pytest

## 📁 Project Structure

```text
job-application-tracker/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── applications.py
│       ├── analytics.py
│       └── auth.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── tests/
│   └── test_applications.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── pytest.ini
├── requirements.txt
└── README.md

```
## ⚙️ Installation
```
1. Clone the repository
git clone https://github.com/Priyavarshni29/job-application-tracker.git
cd job-application-tracker


2. Create a virtual environment

Windows: python -m venv venv
venv\Scripts\activate


3. Install dependencies

pip install -r requirements.txt
```

## 🗄️ Database Setup
This project uses MySQL with SQLAlchemy ORM.

Create the database:
```
CREATE DATABASE job_tracker;
```

Create a .env file using .env.example as a reference:
```
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/job_tracker JWT_SECRET=your_secret_key
```
The .env file contains local credentials and must not be committed to GitHub.


## 🔄 Database Migrations
Apply the database migrations using Alembic:
```
alembic upgrade head
```

## ▶️ Run the Application
Start the FastAPI development server:
```
uvicorn app.main:app --reload
```

The API will be available at:
```
http://127.0.0.1:8000
```

## 📖 API Documentation
FastAPI automatically provides interactive Swagger documentation.
Open:
```
http://127.0.0.1:8000/docs
```

Swagger UI can be used to register users, authenticate, and test protected API endpoints.

## 🔑 Authentication
Register
```
POST /auth/register

Example:
{
    "name": "Priya",
    "email": "priya@example.com",
    "password": "password123"
}
```

Login

```
POST /auth/login
```
The login endpoint verifies the credentials and returns a JWT access token.
```
{
    "access_token": "JWT_TOKEN",
    "token_type": "bearer"
}
```
The token is used to access protected endpoints.

## 🛠️ API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Authenticate user and generate JWT |

### Application Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/applications/` | Create an application |
| GET | `/applications/` | Get active applications |
| GET | `/applications/{id}` | Get an application |
| PUT | `/applications/{id}` | Update an application |
| PATCH | `/applications/{id}/archive` | Archive an application |
| DELETE | `/applications/{id}` | Permanently delete an application |

> All application endpoints require authentication.

## 🔎 Filtering
Applications can be filtered by status:
GET /applications/?status=Interview

Example statuses:
- Applied
- OA
- Interview
- Selected
- Rejected

## ↕️ Sorting
Ascending
```
GET /applications/?sort=asc
```
Descending
```
GET /applications/?sort=desc
```

## 📦 Archive vs Delete
The application tracker distinguishes between archiving and permanent deletion.

Archive
```
PATCH /applications/{id}/archive
```

Archived applications:
```
- Are hidden from the active application list
- Remain stored in the database
- Remain included in analytics
- Preserve application history
```
Delete
```
DELETE /applications/{id}
```

Deleted applications ar:
```
- Permanently removed from the database analytics.
- And from analytics
```

## 📊 Analytics
The analytics endpoint provides statistics for the authenticated user:
```
GET /analytics/
```

It returns:

- Total applications
- Applications grouped by status
- Applications grouped by company
- Interview conversion rate

Example:
```
{
    "total_applications": 10,
    "by_status": {
        "Applied": 5,
        "OA": 2,
        "Interview": 2,
        "Rejected": 1
    },
    "by_company": {
        "Company A": 3,
        "Company B": 2,
        "Company C": 5
    },
    "interview_conversion_rate": 20.0
}
```
Archived applications are included in analytics to preserve historical data.

## 🔒 Security

- JWT Authentication
- Protected endpoints require a valid JWT bearer token.
- Password Hashing
- Passwords are hashed before being stored in the database.
- User Ownership
- Every application belongs to a specific authenticated user.
- A user cannot retrieve, update, or delete another user's applications.
- Environment Variables
- Database credentials and JWT secrets are stored in .env.
- The .env file is excluded from Git using .gitignore.


## 🧪 Testing
Run the automated test suite:
```
pytest
```

Current verified result:
```
3 passed
```

The tests verify:
- Root endpoint
- User registration
- User login
- JWT authentication
- Application creation
- Application retrieval
- Application update
- Application archiving
- Archive visibility behavior
- Analytics preservation
- Permanent deletion
- Ownership authorization
- Prevention of cross-user access

## 🗃️ Database Operations
The application uses SQLAlchemy ORM for database interaction.
Analytics use SQL aggregation operations including:

- COUNT
- GROUP BY


Alembic is used for database schema migrations.


## 🔮 Future Improvements
- Frontend dashboard
- Application search by company and role
- Pagination
- CSV export
- Advanced recruitment analytics
- Application reminders
- Application unarchive functionality
- Dashboard charts and visualizations


