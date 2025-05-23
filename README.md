# Notification Service

A robust, extensible microservice for handling notifications via Email, SMS, and Push channels. This service supports idempotency, dynamic notification templates, provider failover, and OTP (One-Time Password) handling.

## Features
- **Multi-channel notifications:** Send notifications via Email, SMS, and Push.
- **Idempotency:** Prevents duplicate notifications for the same event.
- **Dynamic Templates:** Manage and update notification templates for each channel.
- **Provider Failover:** Automatically switches to backup providers if the primary fails.
- **OTP Handling:** Generate and validate OTPs for secure user verification.
- **Extensible:** Easily add new notification providers or channels.

## Project Structure
- `main.py` – FastAPI application entrypoint and API routes
- `providers/` – Integrations for Email, SMS, and Push providers
- `services/` – Business logic for notifications, templates, OTP, and provider management
- `db_connection/` – Database models, connection, and serialization
- `utils/` – Logging and retry utilities
- `Dockerfile` – Containerization setup
- `requirements.txt` – Python dependencies

## Getting Started

### Prerequisites
- Docker (recommended)
- Or: Python 3.11+ (if you do not want to use Docker)

### 1. Clone the repository
```sh
git clone https://github.com/TurkiHaqawi/notification_service.git
cd notification_service
```

### 2. Set up environment variables
Create a `.env` file in the project root with your configuration (database URL, provider keys, etc.):
```
DATABASE_URL=postgresql://user:password@host:port/dbname
# Add other provider keys and secrets as needed
```

### 3. Run the service (Recommended: Docker)
If you have Docker installed, you can build and run the service easily:
```sh
docker build -t notification_service .
docker run --env-file .env -p 8000:8000 notification_service
```

### 4. Run the service locally (Without Docker)
If you do not have Docker, you can use a Python virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
uvicorn main:app --reload
```

### 5. API Endpoints
- `GET /` – Health check
- `GET /templates` – List all notification templates
- `GET /templates/{template_name}` – Get a specific template
- `PUT /templates/{template_name}` – Update a template
