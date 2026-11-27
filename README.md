# Hotel Management System (Django + React)

Starter project for a hotel website with a Django REST API, PostgreSQL configuration,
Django Admin for employees, and a React/Vite public website.

## Requirements
- Python 3.11+
- Node.js 20+
- PostgreSQL (or use SQLite for initial local testing)

## 1. Backend setup (Windows PowerShell)

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Django API: http://127.0.0.1:8000/api/  
Django Admin: http://127.0.0.1:8000/admin/

The superuser created with `createsuperuser` can access Django Admin. To add another employee,
create a user in Django Admin and enable **Staff status**. Do not enable Staff status for guests.

## 2. Frontend setup

Open a second terminal:

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

React: http://localhost:5173/

## Database
The project uses SQLite by default so it can start without PostgreSQL. To use PostgreSQL,
set `DB_ENGINE=postgres` and configure `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and
`DB_PORT` in `backend/.env`.

## Included
- Public pages: Home, Hotel Info, Booking, Contact, Login, Register, My Reservations
- Room listing and filters (price, dates, beds, floor, view)
- Guest registration/login using JWT
- Reservation creation and overlap protection on the backend
- Contact form
- Hotel information and sponsor models
- Django Admin for rooms, reservations, guests and hotel content
- Basic admin statistics API (staff only)

## Important notes
- This is a development starter, not a production deployment.
- Payment processing is not implemented. Do not collect or store card details.
- Configure production secrets, HTTPS, email delivery, CORS, backups and privacy controls
  before deploying.
- Availability is checked on the server when a reservation is created. For a production
  system with high concurrency, use a database transaction and stronger database-level
  constraints/locking appropriate to the selected database.
