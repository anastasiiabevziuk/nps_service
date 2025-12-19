# 📸 NPS Service (Photo Management System)

A backend service for managing photo sessions, models, and photographers. Built with **FastAPI** and **PostgreSQL**, and fully containerized using **Docker**.

## 🚀 Quick Start

### 1. Prerequisites

Make sure you have **Docker** and **Docker Compose** installed on your machine.

### 2. Environment Setup

Create a `.env` file in the root directory. Use `.env.example` as a template.

### 3. Launch the Project

Run the following command in your terminal:

```bash
docker compose up --build
```

Once started, the service will be available at:

Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

API Endpoint: [http://localhost:8000](http://localhost:8000)

### 🛠 Tech Stack

- Backend: FastAPI (Python 3.10+)

- Database: PostgreSQL 17

- Database Driver: asyncpg (Asynchronous)

- Containerization: Docker & Docker Compose

### 🗄 Database Structure

On the first run, Docker automatically initializes the database using the init.sql file. The schema includes tables within the HR schema:

- model — Model profiles and contact info.

- photographer — Photographer details and equipment.

- photosession — Records of specific photo shoots.
- photo — File paths and image metadata (ISO, Lens, Camera).

### 📸 Media Storage

All uploaded photos are stored locally in the ./uploaded_photos directory. This folder is mounted as a Docker Volume, ensuring that your images persist even after the containers are restarted or removed.

🛠 Useful Commands
Stop services:

```bash
docker compose down
```

Reset database:

```bash
docker compose down -v
```

(Warning: this deletes all stored data!)

View logs:

```bash
docker compose logs -f
```
