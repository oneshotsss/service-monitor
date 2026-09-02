# Service Monitor

**A learning project demonstrating FastAPI, PostgreSQL, Docker, and modern web development.**

## Project Overview

Service Monitor is a backend system that:
- Receives **heartbeats** from multiple Python services running in Docker containers
- Stores heartbeat data and service status in **PostgreSQL**
- Automatically detects when services go **ONLINE** or **OFFLINE**
- Maintains historical records of service state changes
- Provides **REST API** endpoints for querying service metrics
- Includes a simple **HTML/CSS/JS frontend** for visualization
- Runs everything with **Docker Compose** for easy deployment

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Docker Network                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  service-a  │  │  service-b  │  │  service-c  │ │
│  │   (client)   │  │   (client)   │  │   (client)   │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘ │
│         │ heartbeat        │ heartbeat       │ heartbeat│
│         └──────────────────┼───────────────────┘        │
│                            │                            │
│                  ┌─────────▼────────┐                   │
│                  │  FastAPI Backend │                   │
│                  │  (port 8000)     │                   │
│                  └─────────┬────────┘                   │
│                            │                            │
│                  ┌─────────▼────────┐                   │
│                  │   PostgreSQL     │                   │
│                  │   (port 5432)    │                   │
│                  └──────────────────┘                   │
│                            ▲                            │
│                  ┌─────────┴────────┐                   │
│                  │  pgAdmin (GUI)   │                   │
│                  │  (port 5050)     │                   │
│                  └──────────────────┘                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Run with Docker Compose

```bash
git clone https://github.com/oneshotsss/service-monitor.git
cd service-monitor
docker-compose up --build
```

### Access the Application

- **Frontend (Dashboard):** http://localhost:8000/
- **API Docs:** http://localhost:8000/docs
- **pgAdmin (Database UI):** http://localhost:5050/
  - Email: `admin@admin.com`
  - Password: `admin`

## Features

### Backend API Endpoints

**Health Check:**
```bash
GET /health
```

**Service Registration & Listing:**
```bash
POST /services                    # Register a new service
GET /services                     # List all services
GET /services/{service_id}        # Get service details
```

**Heartbeat:**
```bash
POST /heartbeat
# Body: { "service_id": "service-a", "timestamp": "...", "latency_ms": 25 }
```

**Service Metrics:**
```bash
GET /services/{service_id}/metrics      # Latency stats, uptime, etc.
GET /services/{service_id}/heartbeats   # Recent heartbeat history
GET /services/{service_id}/events       # State change history
```

### Frontend Features

- **Dashboard:** Real-time view of all monitored services
- **Service Details:** Click "OPEN" to see detailed metrics for each service
- **Status Monitoring:** Automatically detects ONLINE/OFFLINE status
- **Live Updates:** Page refreshes every 5 seconds

### Database

**Tables:**
- `services` - Monitored services (status, last heartbeat, timestamps)
- `heartbeats` - Heartbeat records (timestamp, latency_ms)
- `service_events` - State change history (ONLINE → OFFLINE transitions)

## Local Development

### Setup

```bash
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up database (PostgreSQL must be running)
# Update DATABASE_URL in app/core/config.py

# Run tests
pytest tests/

# Run backend
uvicorn app.main:app --reload --port 8000
```

### Project Structure

```
service-monitor/
├── app/
│   ├── api/                 # API endpoints
│   │   ├── endpoints/
│   │   │   ├── health.py
│   │   │   ├── services.py
│   │   │   ├── heartbeat.py
│   │   │   ├── services_detail.py
│   │   │   └── frontend.py
│   │   └── router.py
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── service.py
│   │   ├── heartbeat.py
│   │   └── service_event.py
│   ├── schemas/             # Pydantic request/response models
│   │   └── service.py
│   ├── services/            # Business logic
│   │   ├── service_manager.py
│   │   ├── heartbeat_manager.py
│   │   ├── event_manager.py
│   │   ├── metrics_manager.py
│   │   └── status_checker.py    # Background thread for offline detection
│   ├── database/            # DB configuration
│   │   ├── base.py
│   │   └── session.py
│   ├── core/                # Config & settings
│   │   └── config.py
│   ├── templates/           # HTML templates
│   ├── static/              # CSS/JS files
│   └── main.py              # FastAPI app entry point
├── clients/                 # Example client services
│   └── service_a/
│       ├── client.py        # Sends heartbeats
│       ├── Dockerfile
│       └── requirements.txt
├── tests/
│   └── test_api.py          # Pytest test cases
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Backend image
├── requirements.txt         # Python dependencies
└── README.md
```

## Running Tests

```bash
pytest tests/test_api.py -v
```

Tests cover:
- Service registration
- Heartbeat handling
- Service listing and metrics
- Offline detection logic

## Configuration

Edit `app/core/config.py`:

```python
HEARTBEAT_TIMEOUT_SECONDS = 15      # Mark service offline after 15s without heartbeat
STATUS_CHECK_INTERVAL_SECONDS = 5   # Check service status every 5 seconds
```

Edit `docker-compose.yml` to adjust client heartbeat intervals:

```yaml
environment:
  INTERVAL: "5"  # Heartbeat interval in seconds
```

## Learning Points

This project demonstrates:

**FastAPI** - Modern Python web framework  
**SQLAlchemy** - ORM for database modeling  
**PostgreSQL** - Relational database  
**Docker & Docker Compose** - Containerization & orchestration  
**REST API Design** - Endpoints, schemas, responses  
**Background Tasks** - Status checker thread  
**HTML/CSS/JavaScript** - Simple frontend  
**Pytest** - Unit testing  
**Git** - Version control  

## Troubleshooting

**"Internal Server Error" on frontend?**
- Check backend logs: `docker-compose logs backend`
- Ensure pgAdmin port 5050 isn't already in use

**Database tables don't exist?**
```bash
docker-compose down -v  # Remove volume
docker-compose up       # Recreate with clean database
```

**Services not sending heartbeats?**
- Check client logs: `docker-compose logs client-a`
- Verify `BACKEND_URL` in docker-compose.yml is correct

## Dependencies

- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **sqlalchemy** - ORM
- **psycopg** - PostgreSQL adapter
- **jinja2** - Template engine
- **pytest** - Testing framework
- **httpx** - HTTP client for testing

## Deployment Notes

For production:
- Use environment variables for secrets (DATABASE_URL, passwords)
- Add authentication to API endpoints
- Use async database driver (asyncpg) instead of psycopg
- Add proper logging and monitoring
- Use Kubernetes instead of Docker Compose for scaling

@oneshotsss

---
