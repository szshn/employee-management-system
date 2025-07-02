# Employee Management System API

A Django REST Framework API for managing employees, departments, attendance, and performance evaluations.

## Features

- Employee and Department management
- Attendance tracking (Present/Absent/Late)
- Performance evaluations (1-5 rating)
- JWT authentication
- Swagger API documentation
- Docker support with PostgreSQL

## Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose

### Setup

1. Clone and navigate to project
   ```bash
   git clone <repository-url>
   cd employee_project
   ```

2. Create environment file
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

3. Start with Docker
   ```bash
   docker-compose up --build
   ```

4. Access the application
   - API Root: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/
   - Swagger UI: http://localhost:8000/api/schema/swagger-ui/

## API Endpoints
Please refer to Swagger UI (`/api/schema/swagger-ui/`) for the detailed description.
| Description | Method | Endpoint | 
|-------------|--------|----------|
| API root | GET | `/` |
| Employee CRUD | GET/POST  | `/employees/` |
| | GET/PUT/PATCH/DELETE  | `/employees/{id}`|
| Department CRUD | GET/POST  | `/departments/` |
| | GET/PUT/PATCH/DELETE  | `/departments/{id}`|
| Attendance CRUD | GET/POST  | `/attendances/` |
| | GET/PUT/PATCH/DELETE  | `/attendances/{id}`|
| Performance CRUD | GET/POST  | `/performances/` |
| | GET/PUT/PATCH/DELETE  | `/performances/{id}`|
| JWT authentication | POST | `/api/login/` |
| JWT token refresh | POST | `/api/login/refresh` |

## Authentication

Use JWT tokens for API access:

```bash
# Login to request token
POST /api/login/
{
    "username": "your_username",
    "password": "your_password"
}

# Use token in requests
Authorization: Bearer <your_access_token>
```

## Management Commands

```bash
# Setup database
python manage.py setup_db

# Add initial data
python manage.py init_data    # for employees and departments
python manage.py init_reports # for attendance and performance reviews

# Add more data
python manage.py seed_employees
python manage.py seed_reports
```

## Tech Stack

- Django 5.2.3
- Django REST Framework
- PostgreSQL
- JWT Authentication
- drf-spectacular (Swagger)
- Docker