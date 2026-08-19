#!/usr/bin/env bash
set -euo pipefail

docker build \
  -f docker/Dockerfile.insecure \
  -t container-hardening-lab:insecure \
  .

docker build \
  -f docker/Dockerfile.hardened \
  -t container-hardening-lab:hardened \
  .

echo "Built images:"
docker images "container-hardening-lab"
