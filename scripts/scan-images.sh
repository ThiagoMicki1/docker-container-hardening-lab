#!/usr/bin/env bash
set -euo pipefail

mkdir -p reports

echo "Scanning insecure image with Trivy..."
trivy image \
  --no-progress \
  --scanners vuln \
  --table-mode summary \
  --format table \
  --output reports/trivy-insecure-current.txt \
  container-hardening-lab:insecure

echo "Scanning hardened image with Trivy..."
trivy image \
  --no-progress \
  --scanners vuln \
  --table-mode summary \
  --format table \
  --output reports/trivy-hardened-current.txt \
  container-hardening-lab:hardened

echo "Scanning Dockerfiles for misconfigurations..."
trivy config \
  --format table \
  --output reports/trivy-config-current.txt \
  docker

echo "Reports written to:"
echo "  reports/trivy-insecure-current.txt"
echo "  reports/trivy-hardened-current.txt"
echo "  reports/trivy-config-current.txt"
