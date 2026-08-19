# Docker Container Hardening Lab

A beginner-friendly DevSecOps project that compares an intentionally insecure Docker image with a hardened Docker image for the same small Flask web app.

This project demonstrates container security, Docker fundamentals, vulnerability remediation, secure configuration, and security reporting for entry-level DevSecOps, Cloud Security, and Security Engineer roles.

## Overview

The lab includes:

- A simple Python Flask web app
- An intentionally insecure Dockerfile
- A hardened Dockerfile
- Build and run scripts
- Trivy scan instructions
- Real Trivy scan reports and sanitized sample scan reports
- Unit tests and app validation
- Documentation explaining the security decisions

This is a learning lab. The insecure Dockerfile is intentionally unsafe so you can explain what is wrong and how the hardened version improves it.

## Folder Structure

```text
docker-container-hardening-lab/
├── README.md
├── LICENSE
├── .dockerignore
├── .gitattributes
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── app/
│   ├── __init__.py
│   └── app.py
├── docker/
│   ├── Dockerfile.insecure
│   └── Dockerfile.hardened
├── docs/
│   ├── container-security-concepts.md
│   └── security-review.md
├── reports/
│   ├── .gitkeep
│   ├── trivy-config-current.txt
│   ├── trivy-hardened-current.txt
│   ├── trivy-insecure-current.txt
│   ├── trivy-insecure-sample.txt
│   ├── trivy-hardened-sample.txt
│   └── validation-sample.txt
├── scripts/
│   ├── build-images.sh
│   ├── run-hardened.sh
│   ├── run-insecure.sh
│   ├── scan-images.sh
│   └── validate_app.py
└── tests/
    └── test_app.py
```

## Features

- Simple Flask app with `/`, `/health`, and `/config-demo`
- Insecure Dockerfile for security review practice
- Hardened Dockerfile with safer container practices
- Non-root container user in the hardened image
- Smaller base image in the hardened image
- Pinned Python dependencies
- `.dockerignore` to reduce build context risk
- No hardcoded secrets
- Docker healthcheck in the hardened image
- Safer file ownership and permissions
- Trivy scanning commands
- Reproducible Trivy report generation
- Real current Trivy scan summaries
- Sanitized example scan output
- Unit tests and validation script

## Insecure Vs Hardened

| Security Area | Insecure Dockerfile | Hardened Dockerfile |
| --- | --- | --- |
| Base image | Full `python:3.10` image | Smaller `python:3.12-slim-bookworm` image |
| Runtime user | Runs as root | Runs as non-root `appuser` |
| App server | Flask development server | Gunicorn |
| Debug mode | `FLASK_DEBUG=1` | Debug mode not enabled |
| File copy | `COPY . .` | Copies only required files |
| Dependencies | Basic install | Pinned dependencies and `--no-cache-dir` |
| Extra packages | Installs tools like `vim` and `netcat` | Avoids unnecessary OS packages |
| File permissions | Default writable files | Root-owned app files with `0555` permissions |
| Healthcheck | None | Checks `/health` endpoint |
| Build context | Riskier broad context | `.dockerignore` excludes sensitive/noisy files |

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements-dev.txt
```

## Run The App Locally

```bash
python app/app.py
```

Open:

```text
http://127.0.0.1:8000
http://127.0.0.1:8000/health
```

Validate the running app:

```bash
python scripts/validate_app.py http://127.0.0.1:8000
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## Build Docker Images

Bash script:

```bash
bash scripts/build-images.sh
```

Manual commands:

```bash
docker build -f docker/Dockerfile.insecure -t container-hardening-lab:insecure .
docker build -f docker/Dockerfile.hardened -t container-hardening-lab:hardened .
```

## Run Docker Containers

Run the insecure image on port `8001`:

```bash
docker run --rm --name container-hardening-lab-insecure -p 8001:8000 container-hardening-lab:insecure
```

Run the hardened image on port `8002` with extra runtime protections:

```bash
docker run --rm --name container-hardening-lab-hardened -p 8002:8000 --read-only --tmpfs /tmp:rw,noexec,nosuid,size=16m --cap-drop ALL --security-opt no-new-privileges container-hardening-lab:hardened
```

Validate:

```bash
python scripts/validate_app.py http://127.0.0.1:8001
python scripts/validate_app.py http://127.0.0.1:8002
```

## Trivy Scanning

Install Trivy by following the official documentation:

```text
https://trivy.dev/
```

Scan both images:

```bash
trivy image container-hardening-lab:insecure
trivy image container-hardening-lab:hardened
```

Show only high and critical vulnerabilities:

```bash
trivy image --severity HIGH,CRITICAL container-hardening-lab:insecure
trivy image --severity HIGH,CRITICAL container-hardening-lab:hardened
```

Scan Dockerfiles for misconfigurations:

```bash
trivy config docker/Dockerfile.insecure
trivy config docker/Dockerfile.hardened
```

Generate project report files:

```bash
bash scripts/scan-images.sh
```

This writes:

- `reports/trivy-insecure-current.txt`
- `reports/trivy-hardened-current.txt`
- `reports/trivy-config-current.txt`

Trivy image scans should usually be run one at a time because Trivy uses a local cache/database lock. Running multiple scans in parallel can cause a cache lock timeout.

Current reports generated from this lab are included:

- [`reports/trivy-insecure-current.txt`](reports/trivy-insecure-current.txt)
- [`reports/trivy-hardened-current.txt`](reports/trivy-hardened-current.txt)
- [`reports/trivy-config-current.txt`](reports/trivy-config-current.txt)

Sanitized sample reports are also included:

- [`reports/trivy-insecure-sample.txt`](reports/trivy-insecure-sample.txt)
- [`reports/trivy-hardened-sample.txt`](reports/trivy-hardened-sample.txt)

## Current Trivy Results

Generated with Trivy `0.74.0` on `2026-08-19`.

| Scan | Result |
| --- | --- |
| Insecure image vulnerability summary | Debian base image target: 3129 vulnerabilities |
| Hardened image vulnerability summary | Debian base image target: 207 vulnerabilities |
| Dockerfile misconfiguration scan | `Dockerfile.insecure`: 3 findings, `Dockerfile.hardened`: 0 findings |

The goal is not to claim the hardened image has zero vulnerabilities. The goal is to show measurable risk reduction: fewer OS packages, a smaller attack surface, non-root execution, a healthcheck, safer file permissions, and cleaner Dockerfile configuration.

## Security Concepts Learned

This project demonstrates:

- Container least privilege
- Running containers as non-root
- Smaller base images
- Dependency pinning
- Docker build context hygiene
- Avoiding hardcoded secrets
- Docker healthchecks
- Safer file permissions
- Vulnerability scanning with Trivy
- DevSecOps comparison reporting

More detail:

- [`docs/container-security-concepts.md`](docs/container-security-concepts.md)
- [`docs/security-review.md`](docs/security-review.md)

## Future Improvements

- Add GitHub Actions to run tests and Trivy scans
- Add Docker Compose for side-by-side local testing
- Add SBOM generation with Trivy
- Add image signing notes with Cosign
- Add Kubernetes deployment examples with security contexts
- Add Hadolint Dockerfile linting
- Add Dependabot configuration for Python dependencies
- Add CI policy gates for high/critical vulnerabilities

## Disclaimer

This project is for educational and portfolio use. The insecure Dockerfile is intentionally unsafe and should not be used in production.

## References

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Docker build context and .dockerignore](https://docs.docker.com/build/concepts/context/)
- [Docker build best practices](https://docs.docker.com/build/building/best-practices/)
- [Trivy container image scanning](https://trivy.dev/docs/latest/guide/target/container_image/)
