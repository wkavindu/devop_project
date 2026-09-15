# OpsTrack Kubernetes Deployment

This directory contains the Kubernetes manifests used to deploy the OpsTrack incident-management application and MongoDB.

## Architecture

The Kubernetes deployment contains:

- One namespace named `opstrack`
- Two OpsTrack application replicas
- One MongoDB replica
- A ClusterIP Service for OpsTrack
- A ClusterIP Service for MongoDB
- A PersistentVolumeClaim for MongoDB data
- Liveness and readiness probes
- A runtime Kubernetes Secret
- CPU and memory requests and limits
- A non-root container security context

## Requirements

- Kubernetes cluster or Minikube
- `kubectl`
- Docker
- Access to `wkavindu/opstrack:latest`

The OpsTrack image supports both:

- `linux/amd64`
- `linux/arm64`

## Start Minikube

```bash
minikube start
kubectl get nodes

## Kubernetes Deployment

OpsTrack is deployed locally to Kubernetes using Minikube.

The Kubernetes environment includes:

- Two OpsTrack application replicas
- MongoDB with persistent storage
- Internal Services and DNS-based service discovery
- Liveness and readiness probes
- A runtime Kubernetes Secret
- Non-root container security settings
- CPU and memory resource controls
- Multi-platform Docker images for AMD64 and ARM64

The deployment was tested for:

- Automatic pod replacement and self-healing
- Manual scaling from two to five replicas
- `ImagePullBackOff` diagnosis and recovery
- `CrashLoopBackOff` diagnosis
- Application-to-MongoDB connectivity

Deployment instructions are available in [`deploy/k8s/README.md`](deploy/k8s/README.md).