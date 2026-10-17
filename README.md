# Cloud & IAM DevSecOps Portal: CI/CD Pipeline

A small Flask web application with an automated **test, build, scan, publish and deploy** pipeline built on **GitHub Actions** and **Docker**, deployed to **Render**.

**Live demo:** https://cicd-pipeline-yfhq.onrender.com/
*(Free tier: the first request after a period of inactivity can take about a minute.)*

## Pipeline

Every push to `main` runs the workflow in `.github/workflows/cicd.yml`. Pull requests run the test and build/scan stages only; they never publish or deploy.

```
git push
   |
   v
1. Run Unit & IAM Tests --> 2. Build & Scan Docker Image --> 3. Deploy to Cloud (Render)
```

| Stage | What it does |
|-------|--------------|
| 1. Run Unit & IAM Tests | Installs dependencies and runs 4 pytest tests: home page, health endpoint, unauthorized request blocked (401), authorized request allowed |
| 2. Build & Scan Docker Image | Builds the image, scans it with Aqua Trivy (HIGH and CRITICAL findings are reported), and on `main` pushes it to GitHub Container Registry |
| 3. Deploy to Cloud | Triggers a Render deployment through a deploy hook stored as a GitHub Actions secret |

Each stage depends on the previous one. If the tests fail, no image is built and nothing is deployed. I checked this by pushing a deliberately failing test and confirming the deploy job did not run.

## Application

| Endpoint | Purpose |
|----------|---------|
| `/` | Service portal landing page |
| `/health` | Health check |
| `/api/secure-data` | Protected endpoint: requires an `Authorization: Bearer <token>` header, otherwise returns 401 |

The tokens in this project are **simulated demo values** used to show role-based access (admin and viewer). They are not real credentials.

## Tech stack

Python, Flask, Gunicorn, pytest, Docker, Aqua Trivy, GitHub Actions, GitHub Container Registry, Render

## Security practices

- Container runs as a **non-root user**
- Image is scanned for vulnerabilities with **Trivy** on every run
- Render deploy hook is stored in **GitHub Actions Secrets**, not in the code
- Registry login uses the short-lived `GITHUB_TOKEN`
- Protected endpoint rejects requests without a valid token

## Run locally

```bash
git clone https://github.com/dinesh-2002-Dev/cicd-pipeline.git
cd cicd-pipeline
pip install -r requirements.txt
pytest

docker build -t cicd-pipeline .
docker run -p 8000:8000 cicd-pipeline

curl http://localhost:8000/health
curl -i http://localhost:8000/api/secure-data
curl -i -H "Authorization: Bearer admin-secret-123" http://localhost:8000/api/secure-data
```

## What I learned

The first six pipeline runs failed because of missing imports, a wrong pytest command and Dockerfile errors. Reading the logs and fixing each failure until the pipeline went green taught me how CI feedback loops work in practice.

## Possible next steps

- Make the Trivy scan fail the pipeline on critical vulnerabilities
- Load tokens from environment variables instead of the source code
- Tag images with the commit SHA as well as `latest`
- Pin runner and action versions
- Provision the hosting infrastructure with Terraform
