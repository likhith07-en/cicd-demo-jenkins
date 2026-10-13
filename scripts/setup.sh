#!/usr/bin/env bash
# One-command local setup: kind cluster + Jenkins (connected to the cluster network).
# Works on Linux, macOS, and Windows via WSL2.
set -euo pipefail
cd "$(dirname "$0")/.."

for tool in docker kind kubectl; do
  command -v "$tool" >/dev/null || { echo "ERROR: '$tool' is not installed"; exit 1; }
done
docker info >/dev/null 2>&1 || { echo "ERROR: Docker daemon is not running"; exit 1; }

CLUSTER=cicd
if kind get clusters | grep -qx "$CLUSTER"; then
  echo ">> kind cluster '$CLUSTER' already exists"
else
  echo ">> Creating kind cluster '$CLUSTER'"
  kind create cluster --name "$CLUSTER" --config kind/kind-config.yaml
fi

echo ">> Writing kubeconfig (internal address, reachable from Jenkins)"
kind get kubeconfig --internal --name "$CLUSTER" > kubeconfig

echo ">> Starting Jenkins"
cd jenkins
if [ -f .env ]; then
  echo "   (jenkins/.env found -> using Configuration-as-Code: credentials + job auto-created)"
  docker compose -f docker-compose.yml -f docker-compose.casc.yml up -d --build
  AUTO=1
else
  docker compose up -d --build
  AUTO=0
fi
cd ..

docker network connect kind jenkins 2>/dev/null || true

echo
echo "=========================================================="
echo " Jenkins:  http://localhost:8080"
echo " App URL:  http://localhost:8081  (after first deploy)"
if [ "$AUTO" = "0" ]; then
  echo " Unlock password:"
  until docker exec jenkins test -f /var/jenkins_home/secrets/initialAdminPassword 2>/dev/null; do sleep 2; done
  echo "   $(docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword)"
  echo " Next: add credentials 'dockerhub-creds' and 'kubeconfig', create the Pipeline job (see README step 4-5)"
else
  echo " Login: admin / (JENKINS_ADMIN_PASSWORD from jenkins/.env). Job 'cicd-demo' already created."
fi
echo "=========================================================="
