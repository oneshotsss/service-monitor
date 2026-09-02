# Service Monitor

A lightweight service monitoring system for tracking service availability, heartbeat status, response latency, uptime and status history.

The project provides a REST API for registering and monitoring services, automatically detects when a service goes offline, stores monitoring data in PostgreSQL, and provides a web dashboard for viewing service health and metrics.

## Features

* Register and manage monitored services
* Heartbeat-based service monitoring
* Automatic `ONLINE` / `OFFLINE` status detection
* Response latency tracking
* Uptime monitoring
* Service status history
* REST API built with FastAPI
* PostgreSQL database integration
* SQLAlchemy ORM
* Automated tests with pytest
* Docker and Docker Compose support
* Web dashboard for monitoring services
* Swagger / OpenAPI API documentation

## Tech Stack

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **Pydantic**
* **Pytest**
* **Docker**
* **Docker Compose**
* **HTML / CSS / JavaScript**

## Architecture

```text
                    ┌─────────────────┐
                    │ Monitored       │
                    │ Services        │
                    └────────┬────────┘
                             │
                          Heartbeat
                             │
                             ▼
                    ┌─────────────────┐
                    │    FastAPI      │
                    │      API        │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
      ┌───────────────┐             ┌────────────────┐
      │  PostgreSQL   │             │ Status Checker │
      │   Database    │             │  Background    │
      └───────────────┘             └────────────────┘
              │                             │
              └──────────────┬──────────────┘
                             ▼
                    ┌─────────────────┐
                    │   Dashboard     │
                    └─────────────────┘
```

## How It Works

Each monitored service periodically sends a heartbeat request to the API.

The monitoring system records the heartbeat, measures response latency and updates the service status.

If a service stops sending heartbeats within the configured time interval, the background monitoring process automatically marks it as `OFFLINE`.

Service status changes are stored in the database, allowing uptime and historical status information to be analyzed later.

## API

The API provides endpoints for managing monitored services and monitoring their status.

Example operations:

```http
POST   /services
GET    /services
GET    /services/{id}
PUT    /services/{id}
DELETE /services/{id}

POST   /services/{id}/heartbeat
GET    /services/{id}/metrics
GET    /services/{id}/history
```

Interactive API documentation is available through Swagger UI:

```text
/docs
```

## Database

The application uses **PostgreSQL** for persistent storage.

SQLAlchemy is used as the ORM layer for working with the database.

The database stores information such as:

* monitored services
* current service status
* heartbeat timestamps
* response latency
* status changes
* monitoring history

## Testing

The project uses **pytest** for automated testing.

Tests cover API functionality and core monitoring logic, including service management and status changes.

Run the test suite with:

```bash
pytest
```

## Running with Docker

Clone the repository:

```bash
git clone https://github.com/oneshotsss/service-monitor.git
cd service-monitor
```

Start the application:

```bash
docker compose up --build
```

After the containers start, the API and dashboard can be accessed through the configured ports.

To stop the application:

```bash
docker compose down
```

## Project Structure

```text
service-monitor/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   └── services/
│
├── tests/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Screenshots

### Dashboard

*Add a screenshot of the monitoring dashboard here.*

## Future Improvements

Possible improvements include:

* JWT authentication
* User accounts and permissions
* Alert notifications
* Configurable monitoring intervals
* More detailed monitoring metrics
* CI/CD pipeline
* Improved dashboard visualizations
