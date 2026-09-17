# OpsTrack Jenkins Deployment

This directory contains the configuration required to run a self-hosted Jenkins controller with an isolated Docker-in-Docker build engine.

The root-level [`Jenkinsfile`](../../Jenkinsfile) defines the OpsTrack CI/CD pipeline.

## Architecture

The Jenkins environment contains two containers:

- `jenkins`: Jenkins controller, web interface and Docker CLI
- `docker`: isolated Docker daemon used to build application images

Persistent Docker volumes store:

- Jenkins configuration, jobs, plugins and build history
- TLS certificates used between Jenkins and the Docker daemon

Jenkins communicates with the Docker daemon over the private Compose network using TLS on port `2376`. The Docker daemon is not exposed publicly.

## Requirements

- Docker Engine
- Docker Compose
- Approximately 2 GB of available memory
- Port `8080` available
- Access to GitHub and Docker Hub

## Start Jenkins

From the repository root:

```bash
docker compose \
  --file deploy/jenkins/compose.yaml \
  up --detach --build
```

View container status:

```bash
docker compose \
  --file deploy/jenkins/compose.yaml \
  ps
```

View Jenkins logs:

```bash
docker compose \
  --file deploy/jenkins/compose.yaml \
  logs --follow jenkins
```

## Unlock Jenkins

Retrieve the initial setup password:

```bash
docker compose \
  --file deploy/jenkins/compose.yaml \
  exec jenkins \
  cat /var/jenkins_home/secrets/initialAdminPassword
```

Open:

```text
http://SERVER_IP:8080
```

Then:

1. Enter the initial setup password.
2. Install the suggested plugins.
3. Create an administrator account.
4. Save the Jenkins URL.

Never commit the initial password or administrator password to Git.

## Verify Docker Connectivity

```bash
docker compose \
  --file deploy/jenkins/compose.yaml \
  exec jenkins \
  docker version
```

Both client and server information should be displayed.

## Configure Docker Hub Credentials

Create a Docker Hub Personal Access Token with Read and Write permissions.

In Jenkins, navigate to:

```text
Manage Jenkins
→ Credentials
→ System
→ Global credentials
→ Add Credentials
```

Use:

```text
Kind: Username with password
Username: Docker Hub username
Password: Docker Hub access token
ID: dockerhub-credentials
```

The token must remain inside Jenkins Credentials and must never be placed in the `Jenkinsfile`.

## Create the OpsTrack Pipeline

Create a new Jenkins item:

```text
Name: opstrack-pipeline
Type: Pipeline
```

Configure:

```text
Definition: Pipeline script from SCM
SCM: Git
Repository URL: https://github.com/wkavindu/devop_project.git
Branch: */main
Script Path: Jenkinsfile
```

Run the job using **Build Now**.

## Pipeline Stages

The pipeline performs:

1. Repository checkout
2. Python dependency installation in a temporary container
3. Automated pytest execution
4. Docker Compose validation
5. Versioned Docker image build
6. Docker Hub publishing for `main`
7. Temporary local image cleanup

Published tags use:

```text
wkavindu/opstrack:jenkins-BUILD_NUMBER
wkavindu/opstrack:jenkins-latest
```

## Failure Testing

A deliberately failing test was committed temporarily to verify that Jenkins:

- Marked the build as failed
- Skipped later build stages
- Executed the failure post-action
- Returned to green after the test was fixed

## Stop Jenkins

Stop the services while preserving Jenkins data:

```bash
docker compose \
  --file deploy/jenkins/compose.yaml \
  stop
```

Start them again:

```bash
docker compose \
  --file deploy/jenkins/compose.yaml \
  start
```

Remove the containers and network while preserving volumes:

```bash
docker compose \
  --file deploy/jenkins/compose.yaml \
  down
```

Do not use `docker compose down --volumes` unless permanent deletion of Jenkins configuration and build history is intended.

## Security Notes

- Jenkins secrets are stored using Jenkins Credentials.
- The Docker daemon is available only through the internal network.
- TLS protects communication with the Docker daemon.
- The Jenkins controller runs as the non-root `jenkins` user.
- Docker-in-Docker requires privileged mode and is intended here for an isolated learning environment.
- Production environments should normally use dedicated and restricted Jenkins build agents.
