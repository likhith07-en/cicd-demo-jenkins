# End-to-End CI/CD Demo: Jenkins + Docker + Kubernetes

A fully automated production-style CI/CD pipeline. Every `git push` runs isolated unit tests inside Docker, packages a minimal production image, pushes to Docker Hub, rolls out to a local Kubernetes (kind) cluster with zero downtime, runs an automated in-cluster smoke test, and triggers automatic rollback if health checks fail.

```
 git push ──► Jenkins ──► Unit tests ──► Docker build ──► Docker Hub ──► kubectl apply ──► Kubernetes (2 pods)
                │        (in Docker)                                          │
                └────────── rollback on failure ◄──── smoke test ◄────────────┘
```

---

## Project Layout

| Path | Purpose |
|------|---------|
| `app/app.py` | Python Flask microservice: `/` (HTML dashboard), `/health`, `/version` |
| `tests/test_app.py` | Pytest unit test suite |
| `Dockerfile` | Multi-stage build: `test` (runs pytest) and `runtime` (non-root `appuser`, gunicorn) |
| `Jenkinsfile` | Declarative Pipeline: checkout → test → build → push → deploy → smoke test → rollback |
| `k8s/` | Kubernetes manifests: Namespace, Deployment (rolling update, probes, limits), NodePort Service |
| `jenkins/` | Jenkins Dockerfile (Docker CLI + kubectl), Docker Compose, and JCasC auto-config |
| `kind/` | Kind cluster config mapping NodePort `30080` to `localhost:8081` |
| `scripts/` | Shell automation: `setup.sh`, `local-test.sh`, `teardown.sh` |
| `Makefile` | Linux/WSL2 shortcuts (`make help`, `make test`, etc.) |
| `CICD_Demo_Presentation.pptx` | 10-slide enterprise presentation deck |

---

## Prerequisites

Ensure the following tools are installed:
1. **Docker Desktop** (running with Linux containers enabled)
2. **kind** (`kind --version`)
   - *Windows install*: `Invoke-WebRequest -Uri "https://kind.sigs.k8s.io/dl/v0.27.0/kind-windows-amd64" -OutFile "$env:LOCALAPPDATA\Microsoft\WindowsApps\kind.exe"`
3. **kubectl** (`kubectl version --client`)
4. **Docker Hub Account** + Personal Access Token (PAT with *Read, Write, Delete* permissions)
5. **Git & GitHub repository**

---

## Complete Command Guide

### Step 0: Local Test (No Jenkins, No Kubernetes)
Runs unit tests inside Docker, builds the runtime image, starts a local container, and verifies endpoints.

#### Windows (PowerShell)
```powershell
# 1. Run unit tests in Docker
docker build --target test -t cicd-demo:test .

# 2. Build runtime image
docker build --target runtime -t cicd-demo:local .

# 3. Start container
docker run -d --name cicd-demo-smoke -p 5000:5000 cicd-demo:local

# 4. Probe health & version
Invoke-RestMethod http://localhost:5000/health
Invoke-RestMethod http://localhost:5000/version

# 5. Clean up test container
docker rm -f cicd-demo-smoke
```

#### Linux / WSL2 (Bash)
```bash
./scripts/local-test.sh
# or using Makefile:
make local-test
```

---

### Step 1: Configure Git & Docker Hub Credentials

1. Update `DOCKERHUB_USER` in `Jenkinsfile`:
   ```groovy
   DOCKERHUB_USER = 'your-dockerhub-username'
   ```

2. Create `jenkins/.env` (gitignored, contains secrets for Jenkins auto-configuration):
   ```env
   JENKINS_ADMIN_PASSWORD=admin123
   DOCKERHUB_USERNAME=your-dockerhub-username
   DOCKERHUB_TOKEN=your-dockerhub-access-token
   GIT_REPO_URL=https://github.com/your-username/cicd-demo-jenkins.git
   GIT_BRANCH=main
   ```

3. Commit and push code:
   ```bash
   git init
   git add .
   git commit -m "init: CI/CD demo setup"
   git branch -M main
   git remote add origin https://github.com/your-username/cicd-demo-jenkins.git
   git push -u origin main
   ```

---

### Step 2: Create the Kubernetes Cluster & Start Jenkins

#### Windows (PowerShell)
```powershell
# 1. Create kind cluster
kind create cluster --name cicd --config kind/kind-config.yaml

# 2. Generate UTF-8 kubeconfig (internal address reachable by Jenkins)
$content = kind get kubeconfig --internal --name cicd
[System.IO.File]::WriteAllText("$PWD\kubeconfig", ($content -join "`n") + "`n", [System.Text.UTF8Encoding]::new($false))

# 3. Build & start Jenkins with JCasC auto-configuration
docker compose -f jenkins/docker-compose.yml -f jenkins/docker-compose.casc.yml up -d --build

# 4. Connect Jenkins container to the kind network
docker network connect kind jenkins
```

#### Linux / WSL2 (Bash)
```bash
./scripts/setup.sh
# or:
make cluster
```

*Access Jenkins at:* **http://localhost:8080** (Login: `admin` / `admin123`).  
The pipeline job `cicd-demo` and credentials (`dockerhub-creds`, `kubeconfig`) are automatically created via JCasC!

---

### Step 3: Run the Jenkins Pipeline

* **Option A (Web UI):** Open http://localhost:8080 &rarr; Click **cicd-demo** &rarr; Click **Build Now**.
* **Option B (PowerShell CLI):**
  ```powershell
  $cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("admin:admin123"))
  $headers = @{Authorization="Basic $cred"}
  $session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
  $crumbResponse = Invoke-RestMethod -Uri "http://localhost:8080/crumbIssuer/api/json" -Headers $headers -WebSession $session
  $headers[$crumbResponse.crumbRequestField] = $crumbResponse.crumb
  Invoke-WebRequest -Uri "http://localhost:8080/job/cicd-demo/build" -Method POST -Headers $headers -WebSession $session
  ```
* **Option C (Automatic):** Push any commit to your GitHub repository (Jenkins polls every ~2 minutes).

---

### Step 4: Verify the Deployment

```powershell
# Check pods and services in the namespace
kubectl -n cicd-demo get pods,svc

# Check application version endpoint
Invoke-RestMethod http://localhost:8081/version

# Test round-robin load balancing across replicas
1..4 | ForEach-Object { (Invoke-RestMethod -Uri http://localhost:8081/version).pod }
```

* **Live App URL:** http://localhost:8081
* **Health Probe:** http://localhost:8081/health
* **Version & Pod Info:** http://localhost:8081/version

---

### Managing Running Services (Pause, Resume, Clean Up)

#### Pause Services (Stop background containers to free CPU/Memory)
```powershell
docker stop jenkins cicd-control-plane
```

#### Resume Services (Restart containers when ready to work)
```powershell
docker start cicd-control-plane jenkins
```

#### Complete Teardown & Clean Up
```powershell
# Remove Jenkins container and volumes
docker compose -f jenkins/docker-compose.yml down -v

# Delete the kind Kubernetes cluster
kind delete cluster --name cicd

# Remove generated kubeconfig
Remove-Item kubeconfig -ErrorAction SilentlyContinue
```
*(On Linux/macOS, simply run `./scripts/teardown.sh` or `make clean`)*

---

## Presentation Deck

A 10-slide PowerPoint presentation is generated in the root directory:
* [`CICD_Demo_Presentation.pptx`](file:///c:/Users/Krishna%20SREE/Downloads/cicd-demo/CICD_Demo_Presentation.pptx)
* To regenerate the presentation at any time:
  ```powershell
  python generate_presentation.py
  ```
