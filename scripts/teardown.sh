#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
(cd jenkins && docker compose -f docker-compose.yml down -v 2>/dev/null)
kind delete cluster --name cicd 2>/dev/null
rm -f kubeconfig k8s/deployment.rendered.yaml
echo "Cleaned up Jenkins, the kind cluster, and generated files."
