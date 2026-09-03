# HR Staff Management

A full-stack practice project for learning modern backend and frontend development using FastAPI and Next.js. This project focuses on building a realistic HR and staff management system with authentication, role-based access, attendance tracking, leave requests, and scalable features that can be expanded as a real product.

## Overview

This system is designed to manage a company’s staff information and HR operations. The admin manages the platform, creates staff accounts, assigns roles and departments, and monitors employee activities. Staff members log in to their assigned account and use the system to manage their profile, attendance, and leave requests.

This project is intended as a learning playground, so it includes both core features and additional technologies that help improve skills.

---

## Main Features

### 1. Authentication and Authorization

- Admin login
- Staff login
- Account creation by admin only
- Role-based permissions
- JWT access tokens and refresh flow
- Secure password handling
- Session and account management improvements

### 2. Admin Features

- Create and manage staff accounts
- Assign departments and roles
- Manage permissions and access levels
- View staff records and employee information
- Monitor attendance and leave records
- Manage staff status and profile data
- Generate reports and dashboards

### 3. Staff Features

- Login using assigned account
- Update profile information
- View personal dashboard
- Check in and check out
- Track attendance history
- Request leave
- View leave status
- Upload profile image or document

### 4. Attendance Management

- Check-in and check-out records
- Total working hours calculation
- Attendance summary by day, week, or month
- Late check-in tracking
- Missed attendance monitoring
- Staff attendance overview for admin

### 5. Leave Management

- Apply for leave
- Leave type selection
- Approval and rejection flow
- Leave history
- Leave balance tracking
- Admin dashboard for leave processing

### 6. Department and Role Management

- Create departments
- Assign managers and staff
- Organize teams by department
- Role-based access restrictions
- Permission mapping per role

### 7. Profile and File Handling

- Staff profile details
- Upload profile images
- Store uploaded files in Cloudflare R2 or compatible storage
- Image validation and file size management
- Optional Firebase integration for notifications or auth features

---

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy / Alembic
- PostgreSQL
- JWT authentication
- Role-based authorization
- Redis for caching or rate limiting
- Rate limiting middleware
- REST API design
- Validation and error handling

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- API integration with FastAPI
- Protected routes
- Dashboard UI and admin panels
- Form validation and user experience flows

### Cloud and Third-Party Services

- Cloudflare R2 for file storage


### Testing and Quality

- Unit tests
- Integration tests
- API tests with pytest
- Frontend component tests
- End-to-end testing
- Linting and formatting
- CI/CD workflow practices

---

## Architecture

This project is structured as a practical full-stack application:

- Frontend: Next.js application for admin and staff dashboard interfaces
- Backend: FastAPI service for APIs, business logic, auth, and data processing
- Database: PostgreSQL for persistent employee and HR data
- Storage: Cloudflare R2 for employee profile images and uploaded documents
- Authentication: JWT + OAuth support
- Monitoring and security: rate limiting, validation, logging, and error handling

---

## Suggested Project Structure

```bash
hr-staff-management/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── domain/
│   │   ├── repositories/
│   │   ├── routes/
│   │   ├── services/
│   │   └── main.py
│   ├── migrations/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env
│   └── README.md
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   ├── Dockerfile
│   ├── .env.local
│   └── README.md
├── docker-compose.yml
├── .gitignore
├── README.md
├── .env.example
└── .dockerignore
```

> This project runs with Docker Compose using two main containers:
>
> - backend container for the FastAPI service
> - frontend container for the Next.js app

---

## License

This project is for educational and practice purposes.
