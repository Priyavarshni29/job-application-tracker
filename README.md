# Job Application Tracker

A REST API for managing job applications, tracking recruitment stages, and generating application analytics.

## Features

- Create, view, update, and delete job applications
- Track application status and recruitment stages
- Store application, OA, and interview dates
- Store package and additional notes
- Filter applications by status
- Sort applications by application date
- Generate application analytics
- Calculate interview conversion rate
- Automated API testing using pytest
- Interactive API documentation using Swagger UI

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- pytest

## Project Structure

```text
job-application-tracker/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   │
│   └── routes/
│       ├── __init__.py
│       ├── applications.py
│       └── analytics.py
│
├── tests/
│   └── test_applications.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md

Database Setup
This project uses MySQL with SQLAlchemy ORM.
Create the database using the MySQL client:
CREATE DATABASE job_tracker;

Configure the database connection in a .env file:
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/job_tracker

The .env file contains local database credentials and must not be committed to GitHub.
The repository includes .env.example as a configuration template.
Installation
Clone the repository:
git clone https://github.com/YOUR_USERNAME/job-application-tracker.git
cd job-application-tracker

Create a virtual environment:
Windows
python -m venv venv
venv\Scripts\activate

Install the required dependencies:
pip install -r requirements.txt

Create a .env file using .env.example as a reference and configure your MySQL connection.
Run the Application
Start the FastAPI development server:
uvicorn app.main:app --reload

The API will be available at:
http://127.0.0.1:8000

API Documentation
FastAPI automatically provides interactive Swagger documentation.
Open:
http://127.0.0.1:8000/docs

You can use Swagger UI to test all API endpoints directly from the browser.
API Endpoints
Application Management
Method	     Endpoint	               Description
POST	/applications/	Create a new application
GET	/applications/	Retrieve all applications
GET	/applications/{id}	Retrieve an application by ID
PUT	/applications/{id}	Update an application
DELETE	/applications/{id}	Delete an application


Filtering
Applications can be filtered by status:
GET /applications/?status=Interview

Example statuses include:
Applied
OA
Interview
Selected
Rejected

Sorting
Applications can be sorted by application date.
Ascending order:
GET /applications/?sort=asc

Descending order:
GET /applications/?sort=desc

Analytics
The analytics endpoint provides recruitment statistics:
GET /analytics/

It returns:
- Total number of applications
- Application count grouped by status
- Application count grouped by company
- Interview conversion rate
Example response:
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

Example Application
Example request:
{
    "company": "Schneider Electric",
    "role": "Software Engineer",
    "status": "Interview",
    "application_date": "2026-10-04",
    "oa_date": "2026-10-04",
    "interview_date": "2026-10-05",
    "package": "10 LPA",
    "notes": "Cleared OA and moved to interview"
}

Testing
Automated API tests are implemented using pytest and FastAPI TestClient.
Run the test suite:
pytest

Current test coverage includes:
- Root endpoint
- Application creation
- Application retrieval
- Application update
- Application deletion
- Verification that deleted applications return 404
Current test result:
6 passed

Database Operations

The application uses SQLAlchemy ORM for database interaction.
The analytics functionality uses SQL aggregation operations such as:
- COUNT
- GROUP BY
This allows application statistics to be calculated directly from the database.


Security

Database credentials are stored in the local .env file.
The .env file is excluded from version control using .gitignore.
Never commit real database passwords or other credentials to the repository.


Future Improvements
- User authentication and authorization
- Pagination for application records
- Dashboard frontend
- CSV export
- Advanced recruitment analytics
- Application reminders
- Search by company and role

