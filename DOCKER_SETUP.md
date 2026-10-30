# School Portal — Docker Setup Guide

A simple guide for running the backend and frontend with Docker.

---

## Folder Structure

```
testing-new-ideas/
├── backend-school/       ← Django REST API (this repo)
└── Frontend-clean/       ← Next.js Frontend (separate repo)
```

These are **two separate projects** with their own `docker-compose.yml` files. They talk to each other through a shared Docker network.

---

## How Everything Connects

```
Browser
  │
  ├── http://localhost:4000  ──→  Frontend (Next.js + Nginx)
  │                                  │
  │                                  │ /api/ requests are proxied to ↓
  │                                  │
  └── http://localhost (port 80) ──→ Backend (Nginx → Gunicorn → Django)
                                        │
                                        ├── PostgreSQL (database)
                                        ├── Redis (task queue)
                                        └── Celery Worker (background tasks)
```

### Port Map

| Service          | Port | What it does                            |
| ---------------- | ---- | --------------------------------------- |
| Backend Nginx    | 80   | Proxies to Django, serves static/media  |
| Backend Gunicorn | 7000 | Runs Django app (internal, not exposed) |
| PostgreSQL       | 5432 | Database (internal, not exposed)        |
| Redis            | 6379 | Task queue for Celery (internal)        |
| Frontend Nginx   | 4000 | Serves the Next.js app to the browser   |
| Frontend Next.js | 3000 | Next.js server (internal, not exposed)  |

> **Note:** "Internal" means the port is only visible between Docker containers, not from your browser.

---

## What is Nginx in the Backend?

Before Docker, you ran `python manage.py runserver` and accessed `localhost:8000`. Now with Docker, Nginx replaces that — you just type `localhost` (no port number needed).

### Before (without Docker)
```
Browser → localhost:8000 → Django dev server
```
You had to remember port 8000 every time.

### Now (with Docker + Nginx)
```
Browser → localhost (port 80) → Nginx → Gunicorn (:7000) → Django
```
Port 80 is the default HTTP port, so the browser doesn't need a port number. Nginx handles the rest internally.

### What Nginx does:
- **Listens on port 80** — so you just type `localhost` instead of `localhost:8000`
- **Serves static files** — Django admin CSS/JS, media uploads (faster than Python)
- **Forwards API requests** — sends `/api/`, `/admin/` to Gunicorn (Django) on internal port 7000

### Port 7000 is internal only
Port 7000 (Gunicorn) is only visible between Docker containers. You never type `localhost:7000` in the browser. Nginx on port 80 is the only entry point.

---

## Do I Need to Install PostgreSQL, Redis, etc.?

**NO.** You only need **Docker Desktop** installed. Docker downloads and runs PostgreSQL, Redis, Nginx, and everything else automatically inside containers. You do not install any of these on your machine.

The frontend's nginx proxies `/api/` calls to the backend's nginx using the Docker network name `backend-school-nginx-1`.

---

## How to Run

### Step 1: Start the Backend

```bash
cd backend-school
docker compose up --build -d
```

Wait for all containers to be healthy:

```bash
docker compose ps
```

You should see 5 containers: `db`, `redis`, `web`, `worker`, `nginx`.

### Step 2: Start the Frontend

```bash
cd Frontend-clean
docker compose up --build -d
```

### Step 3: Open in Browser

- **Frontend:** http://localhost:4000
- **Backend API:** http://localhost/api/
- **Django Admin:** http://localhost/admin/

---

## If Your Junior Wants to Use Port 8000 (Backend) and Port 3000 (Frontend)

### Change Backend to Port 8000

Edit 3 files in `backend-school/`:

**1. `Dockerfile` — change lines 41 and 43:**

```
EXPOSE 8000
CMD ["gunicorn", "school_core.wsgi:application", "--bind", "0.0.0.0:8000", ...]
```

**2. `docker-compose.yml` — change lines 35 and 37:**

```
command: sh -c "python manage.py migrate && gunicorn school_core.wsgi:application --bind 0.0.0.0:8000 --workers 2"
expose:
  - "8000"
```

**3. `nginx/nginx.conf` — change line 15:**

```
server web:8000;
```

### Change Frontend to Port 3000

Edit `Frontend-clean/docker-compose.yml`:

```yaml
# Change NEXT_PUBLIC_API_URL to use port 3000
NEXT_PUBLIC_API_URL: http://localhost:3000/api

# Change the nginx port mapping
ports:
  - "3000:80"
```

Then rebuild both:

```bash
# Backend
cd backend-school
docker compose down
docker compose up --build -d

# Frontend
cd Frontend-clean
docker compose down
docker compose up --build -d
```

---

## Environment Files

### Backend `.env` (required variables)

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_DB=school_db
POSTGRES_USER=school_user
POSTGRES_PASSWORD=your-db-password
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-app-password
```

### Frontend `.env`

```
NEXT_PUBLIC_API_URL=http://localhost/api
```

> **Important:** `.env` files contain passwords. Never push them to git. Copy `.env.example` to `.env` and fill in your own values.

---

## Useful Commands

```bash
# Check running containers
docker compose ps

# View logs for a specific service
docker compose logs web          # Backend Django
docker compose logs worker       # Celery worker
docker compose logs nginx        # Backend Nginx
docker compose logs frontend     # Frontend Next.js

# Stop everything
docker compose down

# Stop and delete all data (fresh start)
docker compose down -v

# Rebuild after code changes
docker compose up --build -d
```

---

## Troubleshooting

| Problem                          | Solution                                                                                                                                  |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 502 Bad Gateway                  | Check if `web` container is running: `docker compose logs web`                                                                        |
| "Set POSTGRES_PASSWORD in .env"  | Add `POSTGRES_PASSWORD=yourpassword` to `.env`                                                                                        |
| Frontend can't reach backend API | Make sure backend is running first, check the Docker network name in frontend's `docker-compose.yml` matches `backend-school_default` |
| Port already in use              | Stop the other service using that port, or change the port number                                                                         |
