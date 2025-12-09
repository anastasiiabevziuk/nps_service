# NPS Service (Photo Session Management API)

## 🌟 Overview

This is a backend service developed using **FastAPI** and **AsyncPG** for managing photo sessions and individual photo records. The API follows a hierarchical routing structure, allowing for CRUD (Create, Read, Update, Delete) operations on photos nested under their respective photo sessions.

### Key Technologies

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL (Asynchronous access via AsyncPG)
- **Database Tooling:** Alembic (for migrations)
- **Security:** JWT Token Authentication (Implemented via OAuth2)

---

## 🚀 Getting Started

### Prerequisites

You need the following installed on your system:

- Python 3.10+
- PostgreSQL Database
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/anastasiiabevziuk/nps_service.git
cd nps_service
```

### 2. Setup Virtual Environment and Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Database Setup

Ensure your PostgreSQL database is running, the connection details are correct (e.g., in the `.env` file), and that **the necessary tables (`photosession`, `photo`, etc.) are already created** in your database schema.

---

## 🏃 3. Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn main:app --reload
```

The service will be accessible at http://127.0.0.1:8000 (or your configured port).

## 🏃 4. API Endpoints

Documentation

Interactive Documentation (Swagger UI): http://127.0.0.1:8000/docs
