pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
    timeout(time: 20, unit: 'MINUTES')
  }

  // Poll Git every ~2 min (or configure a GitHub webhook instead)
  triggers { pollSCM('H/2 * * * *') }

  environment {
    DOCKERHUB_USER   = 'likhithkumarp07'                   // <-- CHANGED
    IMAGE_NAME       = "${DOCKERHUB_USER}/cicd-demo"
    REGISTRY_CREDS   = 'dockerhub-creds'                  // Jenkins credential ID (username/password)
    KUBECONFIG_CREDS = 'kubeconfig'                       // Jenkins credential ID (secret file)
    K8S_NAMESPACE    = 'cicd-demo'
  }

  stages {

    stage('Checkout') {
      steps {
        checkout scm
        script {
          env.GIT_SHORT = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
          env.IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_SHORT}"
          echo "Image tag: ${env.IMAGE_TAG}"
        }
      }
    }

    stage('Unit Tests') {
      // The Dockerfile 'test' stage runs pytest; a failing test fails the build
      steps {
        sh 'docker build --target test -t ${IMAGE_NAME}:test-${IMAGE_TAG} .'
      }
    }

    stage('Build Image') {
      steps {
        sh '''
          docker build --target runtime \
            --build-arg APP_VERSION=${IMAGE_TAG} \
            -t ${IMAGE_NAME}:${IMAGE_TAG} \
            -t ${IMAGE_NAME}:latest .
        '''
      }
    }

    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: env.REGISTRY_CREDS,
                                          usernameVariable: 'REG_USER',
                                          passwordVariable: 'REG_PASS')]) {
          sh '''
            echo "$REG_PASS" | docker login -u "$REG_USER" --password-stdin
            docker push ${IMAGE_NAME}:${IMAGE_TAG}
            docker push ${IMAGE_NAME}:latest
          '''
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        withCredentials([file(credentialsId: env.KUBECONFIG_CREDS, variable: 'KUBECONFIG')]) {
          sh '''
            sed "s|DOCKER_IMAGE_PLACEHOLDER|${IMAGE_NAME}:${IMAGE_TAG}|" k8s/deployment.yaml > k8s/deployment.rendered.yaml
            kubectl apply -f k8s/namespace.yaml
            kubectl apply -f k8s/deployment.rendered.yaml
            kubectl apply -f k8s/service.yaml
            kubectl -n ${K8S_NAMESPACE} rollout status deployment/cicd-demo --timeout=120s
          '''
          script { env.DEPLOYED = 'true' }
        }
      }
    }

    stage('Smoke Test') {
      steps {
        withCredentials([file(credentialsId: env.KUBECONFIG_CREDS, variable: 'KUBECONFIG')]) {
          sh '''
            kubectl -n ${K8S_NAMESPACE} run smoke-${BUILD_NUMBER} --rm -i --restart=Never \
              --image=curlimages/curl:8.8.0 -- curl -fsS http://cicd-demo/health
          '''
        }
      }
    }
  }

  post {
    failure {
      script {
        if (env.DEPLOYED == 'true') {
          echo 'Deployment unhealthy - rolling back'
          withCredentials([file(credentialsId: env.KUBECONFIG_CREDS, variable: 'KUBECONFIG')]) {
            sh 'kubectl -n ${K8S_NAMESPACE} rollout undo deployment/cicd-demo || true'
          }
        }
      }
    }
    always {
      sh 'docker logout || true'
      sh 'docker rmi ${IMAGE_NAME}:test-${IMAGE_TAG} || true'
    }
  }
}
