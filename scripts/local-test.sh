#!/usr/bin/env bash
# Runs the same steps as the pipeline's test+build stages, then probes the container.
set -euo pipefail
cd "$(dirname "$0")/.."
echo ">> Unit tests (Docker test stage)"; docker build --target test -t cicd-demo:test .
echo ">> Runtime image";                 docker build --target runtime -t cicd-demo:local .
echo ">> Starting container"
docker rm -f cicd-demo-smoke >/dev/null 2>&1 || true
docker run -d --name cicd-demo-smoke -p 5000:5000 cicd-demo:local >/dev/null
trap 'docker rm -f cicd-demo-smoke >/dev/null 2>&1 || true' EXIT
for i in $(seq 1 15); do curl -fs localhost:5000/health >/dev/null && break; sleep 1; done
echo ">> /health  -> $(curl -fs localhost:5000/health)"
echo ">> /version -> $(curl -fs localhost:5000/version)"
echo "PASS"
