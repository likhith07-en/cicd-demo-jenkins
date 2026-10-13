FROM jenkins/jenkins:lts-jdk17
USER root
RUN apt-get update && apt-get install -y ca-certificates curl gnupg \
 && install -m 0755 -d /etc/apt/keyrings \
 && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
 && chmod a+r /etc/apt/keyrings/docker.asc \
 && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo $VERSION_CODENAME) stable" > /etc/apt/sources.list.d/docker.list \
 && apt-get update && apt-get install -y docker-ce-cli docker-buildx-plugin \
 && rm -rf /var/lib/apt/lists/*
RUN ARCH=$(dpkg --print-architecture) \
 && curl --retry 3 --retry-delay 5 -fsSLo /usr/local/bin/kubectl \
    "https://dl.k8s.io/release/$(curl --retry 3 -Ls https://dl.k8s.io/release/stable.txt)/bin/linux/${ARCH}/kubectl" \
 && chmod +x /usr/local/bin/kubectl
USER jenkins
RUN jenkins-plugin-cli --plugins git workflow-aggregator credentials-binding plain-credentials \
    pipeline-stage-view timestamper configuration-as-code job-dsl
