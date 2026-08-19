#!/usr/bin/env bash
set -euo pipefail

trivy image container-hardening-lab:insecure
trivy image container-hardening-lab:hardened

echo "High and critical vulnerability view:"
trivy image --severity HIGH,CRITICAL container-hardening-lab:insecure
trivy image --severity HIGH,CRITICAL container-hardening-lab:hardened
