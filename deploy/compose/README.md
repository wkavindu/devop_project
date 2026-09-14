# Docker Compose Deployment

Docker Compose runs the complete OpsTrack stack:

- Nginx reverse proxy
- Flask/Gunicorn application
- MongoDB database
- Persistent MongoDB volume
- Private frontend and backend networks

## Architecture

Requests follow this path:

Browser → Nginx → OpsTrack → MongoDB → MongoDB volume

Only Nginx publishes a host port. OpsTrack and MongoDB remain inside
the Docker networks.

## Configuration

Create a local `.env` file from `.env.example` and provide a secure
`SECRET_KEY`. Never commit the real `.env` file.

The application connects to MongoDB using the Compose service name:

```text
mongodb://mongo:27017/