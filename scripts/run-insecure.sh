#!/usr/bin/env bash
set -euo pipefail

docker run --rm \
  --name container-hardening-lab-insecure \
  -p 8001:8000 \
  container-hardening-lab:insecure
