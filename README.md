# 🏫 School Management System Backend (`backend-school`)

A robust, modular Django REST Framework backend designed for school management operations, including admissions tracking, faculty directories, and campus notices. Built with a clean **Service–Selector architecture** for maintainable, testable, and scalable business logic.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#-tech-stack)
- [Architecture &amp; Design](#-architecture--design)
- [Recent Updates &amp; Changelog](#-recent-updates--changelog)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation &amp; Setup](#installation--setup)
  - [Running the Server](#running-the-server)
- [API Reference](#-api-reference)
  - [Admissions API](#1-admissions-api)
  - [Faculty API](#2-faculty-api)
  - [Notices API](#3-notices-api)
- [Git Workflow: Preparing to Push](#-git-workflow-preparing-to-push)

---

## 🎯 Overview

The `backend-school` service powers administrative and informational workflows for school portals and client web/mobile applications:

1. **Admissions Management**: Handles student admission inquiries, parent contact details, targeted grades, and status lifecycles (`pending`, `contacted`, `resolved`).
2. **Faculty Management**: Manages academic departments and faculty staff profiles, with active status tracking and relational department data.
3. **Notices & Bulletins**: Categorized announcements (`academic`, `event`, `general`, `urgent`) with prioritized visibility (`Low`, `Medium`, `High`) and URL-friendly slugs.

---

## 🛠️ Tech Stack

- **Framework**: [Django](https://www.djangoproject.com/) 6.1+ & [Django REST Framework (DRF)](https://www.django-rest-framework.org/) 3.18+
- **Database**: SQLite (default for development; compatible with PostgreSQL/MySQL)
- **Environment Management**: `django-environ`
- **CORS Support**: `django-cors-headers`
- **Architecture**: Service–Selector Pattern (separation of queries and mutations)

---

## 🏛️ Architecture & Design

This backend adopts the **Service–Selector Pattern** to decouple Django models and views:

- **Selectors (`selectors.py` / `selector.py`)**: Pure query functions responsible for fetching and filtering data from the database.
- **Services (`services.py`)**: Dedicated business logic layer responsible for creating, updating, or mutating state.
- **Serializers (`serializers.py`)**: Responsible for data parsing, validation, and presentation.
- **Views / ViewSets (`views.py`)**: Thin controllers coordinating request parsing, service/selector invocation, and HTTP responses.

---

## 🚀 Recent Updates & Changelog

Here is a summary of recent changes and enhancements made to `backend-school`:

1. **Service Layer Introduction**:

   - Created `faculty/services.py` with `create_faculty(data)` to handle faculty profile creation.
   - Created `notices/services.py` with `create_notice(data)` to encapsulate notice publication logic.
   - Updated `FacultyViewSet.perform_create` and `NoticeViewSet.perform_create` to delegate directly to their respective service layer functions.
2. **Admissions Service Refactoring**:

   - Refactored `admissions/services.py` (`process_admission_inquiry`) to match the model schema (`parent_name`, `email`, `phone`, `student_grade`).
3. **Faculty Serializer Improvements**:

   - Added write-only `department_id` (`PrimaryKeyRelatedField`) to `FacultySerializer` alongside read-only nested `DepartmentSerializer`. This allows clients to submit department IDs cleanly without sacrificing detailed serialized output.
4. **Notices Selectors Cleanup**:

   - Cleaned up redundant function definitions in `notices/selectors.py` and standardized high-priority queries using `Notice.PriorityLevel.HIGH`.
5. **Environment & Security**:

   - Added `.env.example` providing standard configuration templates for `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS`.
   - Updated CORS settings in `school_core/settings.py` allowing frontend connectivity (e.g. `http://localhost:3000`).

---

## 📁 Project Structure

```text
backend-school/
├── .env.example             # Template for environment variables
├── .gitignore               # Ignored files (virtualenvs, .env, db.sqlite3)
├── requirements.txt         # Python package dependencies
├── manage.py                # Django CLI utility
├── school_core/             # Core project configuration
│   ├── settings.py          # App settings, CORS, DRF, Database config
│   ├── urls.py              # Root router and API endpoints
│   ├── wsgi.py              # WSGI entry point
│   └── asgi.py              # ASGI entry point
├── admissions/              # Admissions inquiry module
│   ├── models.py            # AdmissionInquiry model
│   ├── serializers.py       # Serializer definitions
│   ├── selectors.py         # Query selectors
│   ├── services.py          # Business logic & inquiry processing
│   └── views.py             # AdmissionInquiryViewSet
├── faculty/                 # Faculty & department module
│   ├── models.py            # Department, Faculty models
│   ├── serializers.py       # Serializers with department_id support
│   ├── selector.py          # Query selectors
│   ├── services.py          # Faculty creation service
│   └── views.py             # FacultyViewSet
└── notices/                 # Campus notices & bulletin module
    ├── models.py            # Notice model (Category, PriorityLevel)
    ├── serializers.py       # NoticeSerializer
    ├── selectors.py         # Filter & priority selectors
    ├── services.py          # Notice creation service
    └── views.py             # NoticeViewSet
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.10+
- `pip` package manager
- `git`

### Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd backend-school
   ```
2. **Create and activate a virtual environment**:

   - On Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - On Linux / macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables**:
   Create a `.env` file from the example template:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` as needed:

   ```env
   SECRET_KEY=your-secure-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```
5. **Apply database migrations**:

   ```bash
   python manage.py migrate
   ```
6. **Create an administrative superuser**:

   ```bash
   python manage.py createsuperuser
   ```

### Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

The server will be available at: `http://127.0.0.1:8000/`
The Django Admin panel is accessible at: `http://127.0.0.1:8000/admin/`

---

## 📡 API Reference

Base API prefix: `/api/`

All list endpoints include page pagination with default page size of `10`.

### 1. Admissions API

- **List Inquiries**: `GET /api/admissions/`
- **Create Inquiry**: `POST /api/admissions/`
- **Retrieve Inquiry**: `GET /api/admissions/{id}/`
- **Update Inquiry**: `PATCH /api/admissions/{id}/`
- **Delete Inquiry**: `DELETE /api/admissions/{id}/`

#### Create Admission Inquiry Payload

```json
{
  "parent_name": "Jane Doe",
  "email": "jane.doe@example.com",
  "phone": "+1234567890",
  "student_grade": "Grade 5"
}
```

### 2. Faculty API

- **List Faculty**: `GET /api/faculty/`
- **Create Faculty**: `POST /api/faculty/`
- **Retrieve Faculty**: `GET /api/faculty/{id}/`
- **Update Faculty**: `PATCH /api/faculty/{id}/`
- **Delete Faculty**: `DELETE /api/faculty/{id}/`

#### Create Faculty Payload

```json
{
  "name": "Dr. Sarah Connor",
  "email": "sconnor@school.edu",
  "phone": "+1987654321",
  "department_id": 1,
  "is_active": true
}
```

### 3. Notices API

- **List Notices**: `GET /api/notices/`
- **Create Notice**: `POST /api/notices/`
- **Retrieve Notice**: `GET /api/notices/{id}/`
- **Update Notice**: `PATCH /api/notices/{id}/`
- **Delete Notice**: `DELETE /api/notices/{id}/`

#### Create Notice Payload

```json
{
  "title": "Annual Sports Day 2026",
  "slug": "annual-sports-day-2026",
  "content": "Join us for the annual sports day event next Friday.",
  "category": "event",
  "priority_level": 2
}
```

**Notice Categories**: `academic`, `event`, `general`, `urgent`
**Priority Levels**: `1` (Low), `2` (Medium), `3` (High)

---

## 🚀 Git Workflow: Preparing to Push

To push your local changes to the remote repository, execute the following commands in your terminal:

```bash
c	# 1. Review status
git status

# 2. Stage updated files and the new README
git add README.md .env.example admissions/ faculty/ notices/ school_core/ requirements.txt

# 3. Commit the changes
git commit -m "feat: add service layer architecture, env configuration, and comprehensive README"

# 4. Push to remote
git push origin mainS
```
