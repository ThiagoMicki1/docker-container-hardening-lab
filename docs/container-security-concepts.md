# Container Security Concepts

This lab compares an intentionally insecure Dockerfile with a hardened Dockerfile for the same small Flask web app.

## Least Privilege

Containers should run with the minimum permissions needed.

In this lab:

- The insecure image runs as root.
- The hardened image creates `appuser` and uses `USER appuser`.

Why it matters:

If an attacker compromises the app, a non-root container user limits what they can do inside the container.

## Smaller Base Images

Large base images often include more packages than an app needs.

In this lab:

- The insecure image uses `python:3.10`.
- The hardened image uses `python:3.12-slim-bookworm`.

Why it matters:

Smaller images usually have fewer packages, fewer vulnerabilities, and less attack surface.

## Dependency Pinning

Pinned dependencies make builds more predictable.

In this lab:

- `requirements.txt` pins `Flask` and `gunicorn`.
- The hardened Dockerfile pins `pip`.

Why it matters:

Predictable builds are easier to scan, troubleshoot, and reproduce.

## Build Context Hygiene

Docker sends a build context to the Docker daemon when building an image.

In this lab:

- `.dockerignore` excludes Git files, virtual environments, tests, reports, logs, and environment files.

Why it matters:

Ignoring unnecessary files makes builds faster and reduces the chance of copying sensitive data into an image.

## Avoiding Hardcoded Secrets

Images should not contain passwords, API keys, tokens, or private data.

In this lab:

- The app contains no real secrets.
- `.gitignore` and `.dockerignore` exclude `.env`, `*.pem`, and `*.key`.

Why it matters:

Secrets baked into images can leak through registries, logs, image layers, and source control.

## Healthchecks

Docker `HEALTHCHECK` defines how Docker can test whether a container is healthy.

In this lab:

- The hardened image checks `http://127.0.0.1:8000/health`.

Why it matters:

Healthchecks help operations and orchestration systems detect broken containers.

## File Permissions

Runtime users should not be able to modify application code unless required.

In this lab:

- The hardened image sets `/app` ownership to `root:root`.
- The hardened image sets app files to read/execute only with `chmod -R 0555 /app`.
- The app runs as `appuser`.

Why it matters:

If the app process is compromised, the attacker should not be able to rewrite application files easily.

## Runtime Hardening

Some protections are applied when the container starts.

The hardened run command includes:

```bash
--read-only
--tmpfs /tmp:rw,noexec,nosuid,size=16m
--cap-drop ALL
--security-opt no-new-privileges
```

Why it matters:

These settings reduce what the container can write, what Linux capabilities it has, and whether it can gain extra privileges. The small `/tmp` tmpfs gives Gunicorn a temporary writable location while keeping the rest of the container filesystem read-only.

## Vulnerability Scanning

Trivy can scan container images for vulnerabilities and misconfigurations.

Example:

```bash
trivy image container-hardening-lab:hardened
```

Why it matters:

Scanning helps DevSecOps teams identify vulnerable packages before images are deployed.
