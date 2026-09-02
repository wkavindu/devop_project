# OpsTrack Deployment

This directory contains the deployment configurations used to run OpsTrack on
Ubuntu 24.04 LTS.

## Architecture

Client requests enter through Nginx on port 80. Nginx forwards them to Gunicorn
on the private loopback interface at `127.0.0.1:5000`. Gunicorn runs the Flask
application, which connects to MongoDB on `127.0.0.1:27017`.

```text
Client
  -> Nginx :80
  -> Gunicorn 127.0.0.1:5000
  -> Flask
  -> MongoDB 127.0.0.1:27017

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