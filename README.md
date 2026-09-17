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

## DevOps implementation progress

- [x] Build and test the local Flask and MongoDB application
- [x] Deploy the application as a hardened systemd service
- [x] Configure automatic startup and failure recovery
- [x] Configure Nginx as a reverse proxy
- [x] Restrict Gunicorn to the loopback interface
- [x] Reproduce and diagnose a 502 Bad Gateway
- [ ] Containerize the application with Docker
- [ ] Orchestrate the stack with Docker Compose
- [ ] Implement CI with GitHub Actions
- [ ] Deploy to Kubernetes
- [ ] Deploy to AWS
- [ ] Implement Jenkins and Ansible
- [ ] Complete continuous deployment and monitoring

## Docker

OpsTrack is packaged as a multi-stage Docker image and runs as a
non-root user with an application health check.

### Build the image

```bash
docker build --tag opstrack:v1 .

## Jenkins CI/CD

OpsTrack includes a self-hosted Jenkins declarative pipeline that:

- Checks out source code from GitHub
- Runs automated tests in an isolated Python container
- Validates the Docker Compose configuration
- Builds versioned Docker images
- Uses Jenkins Credentials for Docker Hub authentication
- Publishes successful `main` builds to Docker Hub
- Reports failures and prevents later stages from running

The Jenkins controller runs with an isolated Docker-in-Docker build engine using TLS and persistent volumes.

See [`deploy/jenkins/README.md`](deploy/jenkins/README.md) for setup instructions.

## Ansible Infrastructure Automation

OpsTrack includes an idempotent Ansible deployment that converts a clean Ubuntu server into a working application server with one command.

The playbook:

- Installs and enables Docker
- Deploys Nginx, OpsTrack and MongoDB with Docker Compose
- Generates and protects the application secret
- Configures persistent MongoDB storage
- Verifies health and database readiness
- Produces `changed=0` when run again against an already configured server

See [`deploy/ansible/README.md`](deploy/ansible/README.md) for deployment instructions.