# Dockerfile Security Review

This document explains the security differences between the intentionally insecure Dockerfile and the hardened Dockerfile.

## Insecure Dockerfile Issues

File: `docker/Dockerfile.insecure`

| Issue | Why It Matters |
| --- | --- |
| Uses `python:3.10` full image | Larger image with more packages and more attack surface |
| Installs unnecessary tools like `vim` and `netcat` | Extra tools can help an attacker explore or pivot inside a compromised container |
| Uses `COPY . .` | May copy unnecessary files, reports, tests, local config, or secrets into the image |
| Runs `pip install` without `--no-cache-dir` | Leaves package cache behind and increases image size |
| Enables `FLASK_DEBUG=1` | Debug mode can expose sensitive error details |
| Runs as root | A compromised app has unnecessary privileges inside the container |
| Uses Flask development server | The dev server is not intended for production-style serving |
| No healthcheck | Docker has no built-in way to tell if the app is healthy |

## Hardened Dockerfile Improvements

File: `docker/Dockerfile.hardened`

| Improvement | Security Benefit |
| --- | --- |
| Uses `python:3.12-slim-bookworm` | Smaller base image with less attack surface |
| Pins dependencies | Builds are more predictable and easier to scan |
| Copies dependency file before app code | Improves build cache behavior |
| Uses `pip install --no-cache-dir` | Reduces image size and leftover package cache |
| Creates `appuser` and `appgroup` | Gives the app a dedicated unprivileged runtime identity |
| Uses `USER appuser` | Runs the app without root privileges |
| Uses `gunicorn` | Uses a production-style Python WSGI server |
| Sets app files to `root:root` and `0555` | Runtime user cannot easily modify application code |
| Adds `HEALTHCHECK` | Provides a built-in container health signal |
| Avoids debug mode | Reduces risk of exposing stack traces or internal details |

## Insecure Vs Hardened Summary

| Area | Insecure Image | Hardened Image |
| --- | --- | --- |
| Base image | `python:3.10` | `python:3.12-slim-bookworm` |
| Runtime user | root | non-root `appuser` |
| Dependency install | basic `pip install` | `pip install --no-cache-dir` |
| File copy | `COPY . .` | only required files copied |
| File permissions | default writable app files | root-owned, read/execute app files |
| Server | Flask dev server | Gunicorn |
| Debug mode | enabled | disabled |
| Healthcheck | none | `/health` endpoint check |
| Build context | riskier broad copy | controlled with `.dockerignore` |

## Mentor Notes

This lab is not saying every real production container must look exactly like this hardened Dockerfile. Instead, it teaches the security reasoning behind common hardening decisions.

In real teams, you would also consider:

- signed images
- SBOM generation
- CI/CD image scanning
- runtime monitoring
- Kubernetes security contexts
- secret managers
- dependency update automation
