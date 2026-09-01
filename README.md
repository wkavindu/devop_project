# OpsTrack

OpsTrack is a Flask and MongoDB incident-tracking application built as the foundation for an end-to-end DevOps portfolio project. It provides incident CRUD workflows, severity and status management, and health endpoints suitable for containers, load balancers, and Kubernetes probes.

## Features

- Create, view, update, and delete incidents
- Track affected service, severity, status, and timestamps
- Responsive operations dashboard
- `GET /health` for application liveness
- `GET /ready` for MongoDB readiness
- Environment-variable configuration
- Automated Flask tests using an isolated mock database

## Run locally

Prerequisites: Python 3.11+ and MongoDB running on `localhost:27017`.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
python run.py
```

Open <http://localhost:5000>. Check the service with:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/ready
```

## Test

```bash
pytest -q
```

The tests do not require a running MongoDB instance.

## Production entry point

```bash
gunicorn --bind 0.0.0.0:5000 run:app
```

## DevOps roadmap

This application is intentionally structured for subsequent stages: Linux and systemd, Nginx, Docker and Compose, GitHub Actions, Kubernetes, AWS, Jenkins, Ansible, monitoring, and security hardening.
