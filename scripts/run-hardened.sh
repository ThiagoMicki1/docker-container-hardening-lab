#!/usr/bin/env bash
set -euo pipefail

docker run --rm \
  --name container-hardening-lab-hardened \
  -p 8002:8000 \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=16m \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  container-hardening-lab:hardened
