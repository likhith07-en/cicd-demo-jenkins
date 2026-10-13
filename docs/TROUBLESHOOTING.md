# Troubleshooting

| Symptom | Cause / Fix |
|---|---|
| `permission denied ... /var/run/docker.sock` in Jenkins | Compose file runs Jenkins as `root` for the demo. Recreate: `docker compose up -d --force-recreate`. |
| `Unable to connect to the server` / `dial tcp 127.0.0.1` in Deploy stage | kubeconfig uses `localhost`. Regenerate with `kind get kubeconfig --internal --name cicd > kubeconfig`, re-upload the credential, and run `docker network connect kind jenkins`. |
| `ImagePullBackOff` | The image repo is private or `DOCKERHUB_USER` is wrong. Make the Docker Hub repo public, or create an imagePullSecret. For no-registry testing use `make deploy-local`. |
| `denied: requested access to the resource is denied` on push | Wrong Docker Hub user/token in `dockerhub-creds`, or `DOCKERHUB_USER` in the Jenkinsfile doesn't match. Use an access token with Read/Write scope. |
| Pipeline can't find credentials | Credential IDs must be exactly `dockerhub-creds` and `kubeconfig`. |
| `localhost:8081` not responding | The cluster must be created with `kind/kind-config.yaml` (it maps NodePort 30080 to 8081). Otherwise use `kubectl -n cicd-demo port-forward svc/cicd-demo 8081:80`. |
| Rollout times out | `kubectl -n cicd-demo describe pod -l app=cicd-demo` and `make logs`. Usually image pull or failing `/health`. |
| Port 8080 already in use | Change the left side of `8080:8080` in `jenkins/docker-compose.yml`. |
| Apple Silicon / ARM | Images are multi-arch (python, jenkins, kubectl are fetched per-arch); no changes needed. |
| JCasC startup error | Check `docker logs jenkins`. Make sure `jenkins/.env` has all variables and `kubeconfig` exists at project root (run `scripts/setup.sh` once, or `kind get kubeconfig --internal --name cicd > kubeconfig`). Delete `jenkins/.env` to fall back to manual setup. |
