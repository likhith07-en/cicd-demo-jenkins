# End-to-End CI/CD Demo: Jenkins + Docker + Kubernetes

A small Flask app plus a fully automated pipeline. Every `git push` is tested, packaged into a Docker image, pushed to a registry, and rolled out to Kubernetes, with automatic rollback if the release is unhealthy.

```
 git push ──► Jenkins ──► Unit tests ──► Docker build ──► Docker Hub ──► kubectl apply ──► Kubernetes (2 pods)
                │        (in Docker)                                          │
                └────────── rollback on failure ◄──── smoke test ◄────────────┘
```

## Project layout

| Path | Purpose |
|------|---------|
| `app/app.py` | Flask app: `/` (HTML page), `/health`, `/version` |
| `tests/` | pytest unit tests |
| `Dockerfile` | Multi-stage: `test` (runs pytest) and `runtime` (non-root, gunicorn) |
| `Jenkinsfile` | Pipeline: checkout → test → build → push → deploy → smoke test → rollback on failure |
| `k8s/` | Namespace, Deployment (rolling update, probes, limits), NodePort Service |
| `k8s/optional/` | HPA (autoscaling) and Ingress examples |
| `jenkins/` | Jenkins image with docker CLI + kubectl; compose files; optional JCasC auto-config |
| `kind/` | Local cluster config exposing the app on `localhost:8081` |
| `scripts/` | `setup.sh`, `teardown.sh`, `local-test.sh` |
| `Makefile` | Shortcuts (`make help`) |
| `docs/TROUBLESHOOTING.md` | Common errors and fixes |

## Prerequisites
Docker, [kind](https://kind.sigs.k8s.io/), kubectl, a Docker Hub account (+ access token), and a Git repo (GitHub etc.). On Windows use WSL2.

## Step 0. Try it locally (no Jenkins, no cluster)
```bash
make local-test        # runs tests, builds the image, starts it, probes /health and /version
```

## Step 1. Put the project in Git and set your Docker Hub user
1. Edit `DOCKERHUB_USER` at the top of the `Jenkinsfile`.
2. `git init && git add . && git commit -m "init"`, then push to your repo.

## Step 2. Create the cluster and Jenkins

### Option A: Automatic (recommended)
```bash
cp jenkins/.env.example jenkins/.env      # fill in Docker Hub token, repo URL, admin password
./scripts/setup.sh
```
This creates the kind cluster, generates `kubeconfig`, starts Jenkins, connects it to the cluster network, and (via Configuration-as-Code) **auto-creates the `dockerhub-creds` and `kubeconfig` credentials and the `cicd-demo` pipeline job**. Log in at http://localhost:8080 as `admin`.

### Option B: Manual
```bash
./scripts/setup.sh                        # without jenkins/.env it prints the unlock password
```
Then in Jenkins (http://localhost:8080): install suggested plugins, and add credentials under **Manage Jenkins → Credentials → Global**:

| ID | Kind | Value |
|----|------|-------|
| `dockerhub-creds` | Username with password | Docker Hub user + access token |
| `kubeconfig` | Secret file | the generated `kubeconfig` file |

Create the job: **New Item → Pipeline → Pipeline script from SCM → Git** → your repo URL, branch, script path `Jenkinsfile`.

## Step 3. Run the pipeline
Click **Build Now** (or push a commit; the job polls Git every ~2 minutes, or add a webhook to `http://<host>:8080/github-webhook/`).

## Step 4. Verify
```bash
make status                        # pods and service
curl http://localhost:8081/version
```
Refresh http://localhost:8081 to see different pod names answering (load balancing).

## Demo scenarios
1. **Auto-deploy:** change the heading in `app/app.py`, commit, push. A new build runs and the page shows the new version tag.
2. **Test gate:** break a test and push. The pipeline stops at *Unit Tests* and nothing is deployed.
3. **Rollback:** make `/health` return HTTP 500 and push. The rollout fails and Jenkins runs `kubectl rollout undo`.
4. **Autoscaling (optional):** install metrics-server, `kubectl apply -f k8s/optional/hpa.yaml`.

## Deploy without Jenkins (quick check of the K8s side)
```bash
make deploy-local                  # builds image, loads it into kind, applies manifests
```

## Cleanup
```bash
make clean
```

## Security notes (read before reusing)
This is a teaching setup. Jenkins runs as root with the host Docker socket, and the kubeconfig is cluster-admin. For real use: Kaniko/rootless builders or dedicated agents, a private registry with image scanning (Trivy), a namespaced ServiceAccount token instead of an admin kubeconfig, Ingress with TLS, and Helm or Argo CD for GitOps. `kubeconfig` and `jenkins/.env` are git-ignored and docker-ignored; never commit them.

## Known limitations
Verified: unit tests, app startup under gunicorn, YAML/shell/Makefile syntax. The Jenkins, Docker, and kind steps depend on your local environment; if something fails see `docs/TROUBLESHOOTING.md`.
