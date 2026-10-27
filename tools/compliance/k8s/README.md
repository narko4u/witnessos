# WitnessOS Compliance Pack — Kubernetes Deployment Guide

> Deploy the compliance scanner for autonomous AI agents on Kubernetes.

## Prerequisites

- Kubernetes cluster (v1.21+)
- `kubectl` configured for your cluster
- Container registry access (or local image build with Minikube / kind)

## Quick Start

### 1. Create the ConfigMap

```bash
kubectl apply -f k8s/configmap.yaml
```

This creates `witnessos-compliance-config` — a ConfigMap with default values for:

- **Scanner interval:** how often compliance scans run
- **Gateway URL:** where to find the WitnessOS Gateway for live evidence
- **Output format:** default report format (json, text, or md)
- **Standards:** which compliance standards to check

### 2. Deploy the Scanner

```bash
kubectl apply -f k8s/deployment.yaml
```

This creates:

- A **Deployment** (`witnessos-compliance`) with 1 replica
- A **Service** (`witnessos-compliance`) exposing port 8080 (ClusterIP)

### 3. Verify the Deployment

```bash
# Check pod status
kubectl get pods -l app=witnessos-compliance

# Check logs
kubectl logs -l app=witnessos-compliance

# Port-forward to test health endpoint
kubectl port-forward svc/witnessos-compliance 8080:8080
# Then visit http://localhost:8080/health
```

## Configuration

Edit `k8s/configmap.yaml` to customise the scanner for your environment:

| Key                 | Default                           | Description                              |
|---------------------|-----------------------------------|------------------------------------------|
| scanner.interval    | `30m`                             | How often to run compliance scans        |
| gateway.url         | `http://witnessos-gateway:8100`   | WitnessOS Gateway address                |
| output.format       | `json`                            | Default report output format             |
| output.directory    | `/data/reports`                   | Where reports are written                |

Apply changes:

```bash
kubectl apply -f k8s/configmap.yaml
# Roll out the deployment to pick up new config
kubectl rollout restart deployment witnessos-compliance
```

## Resource Limits

The deployment sets conservative defaults:

| Resource | Limit   | Request |
|----------|---------|---------|
| Memory   | 256 Mi  | 128 Mi  |
| CPU      | 500 m   | 250 m   |

Adjust in `k8s/deployment.yaml` based on your workload.

## Building the Docker Image

```bash
# From the repo root
docker build -t witnessos-compliance:0.1.0 -f docker/Dockerfile .
```

Or push to your registry:

```bash
docker tag witnessos-compliance:0.1.0 registry.example.com/witnessos-compliance:0.1.0
docker push registry.example.com/witnessos-compliance:0.1.0
```

Then update `image:` in `k8s/deployment.yaml` to point to your registry.

## Using the CLI Inside the Cluster

Run ad-hoc compliance commands inside the pod:

```bash
# List available standards
kubectl exec -it deployment/witnessos-compliance -- witnessos-compliance list

# Generate an NSA MCP compliance report
kubectl exec -it deployment/witnessos-compliance -- witnessos-compliance report --standard nsa-mcp
```

## Uninstall

```bash
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/configmap.yaml
```
