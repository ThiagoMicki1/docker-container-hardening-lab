#!/usr/bin/env bash
set -euo pipefail

mkdir -p reports

echo "Generating CycloneDX SBOM for hardened image..."
trivy image \
  --no-progress \
  --format cyclonedx \
  --output reports/container-hardening-lab-hardened-sbom.cdx.json \
  container-hardening-lab:hardened

echo "SBOM written to:"
echo "  reports/container-hardening-lab-hardened-sbom.cdx.json"
