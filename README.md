# Simple Flask API

A small Flask REST API with unit tests, Docker packaging, Kubernetes manifests, and a Helm chart.

## API Endpoints

- `GET /api/health` returns service health.
- `GET /api/greet?name=Sayan` returns a greeting. If `name` is omitted, it defaults to `World`.
- `POST /api/add` accepts JSON with numeric `a` and `b` fields and returns their sum.

Example:

```bash
curl http://localhost:5000/api/health
curl "http://localhost:5000/api/greet?name=Sayan"
curl -X POST http://localhost:5000/api/add \
  -H "Content-Type: application/json" \
  -d '{"a": 7, "b": 5}'
```

## Project Layout

```text
src/app.py                         Flask application
src/test_app.py                    Pytest tests
Dockerfile                         Container image definition
requirements.txt                   Python dependencies
k8s/                               Raw Kubernetes manifests
charts/SimpleFlaskAPI/             Helm chart for this Flask API
charts/argo/values-argo.yaml       Argo CD Helm values
```

## Local Development

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the app:

```bash
python src/app.py
```

The API listens on:

```text
http://localhost:5000
```

Run tests:

```bash
pytest
```

## Docker

Build the image:

```bash
docker build -t simple-flask-api:v1 .
```

Run the container:

```bash
docker run --rm -p 5000:5000 simple-flask-api:v1
```

The Helm chart currently points to this image:

```text
sayansarkar1992/simple-flask-app:v1
```

## Kubernetes Manifests

Deploy using the raw manifests:

```bash
kubectl create namespace python-app
kubectl apply -f k8s/ -n python-app
kubectl get pods -n python-app
```

The raw manifests create:

- Deployment: `simple-flask-app`
- Service: `simple-flask-app`
- Ingress: `simple-flask-app-ingress`
- Host: `simple-flask.local`

## Helm Deployment

Install or upgrade the Flask API chart:

```bash
helm upgrade --install simple-flask-api ./charts/SimpleFlaskAPI \
  -n python-app \
  --create-namespace
```

Check the deployed resources:

```bash
kubectl get all -n python-app
kubectl get ingress -n python-app
```

Render the chart locally before applying:

```bash
helm template simple-flask-api ./charts/SimpleFlaskAPI -n python-app
```

Validate the chart:

```bash
helm lint ./charts/SimpleFlaskAPI
```

## Argo CD

The Argo CD values file is located at:

```text
charts/argo/values-argo.yaml
```

Install or upgrade Argo CD with those values:

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

helm upgrade --install argocd argo/argo-cd \
  -n argocd \
  --create-namespace \
  -f ./charts/argo/values-argo.yaml
```

Get the initial admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
```

Port-forward the Argo CD UI:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Then open:

```text
https://localhost:8080
```

Default username:

```text
admin
```

## Notes

- Use lowercase Helm release names such as `simple-flask-api`.
- Use `./charts/SimpleFlaskAPI` for the local chart path. Without `./`, Helm treats `charts/SimpleFlaskAPI` as a repository chart reference.
- The Flask app health endpoint is `/api/health`, and the Helm probes are configured to use that path.
