pipeline {
  agent any
  environment {
    IMAGENAME = 'joepetraa/mobile-app'
    REGISTRY = 'https://index.docker.io/v1/'
    REGISTRYCREDENTIALS = 'dockerhub-credentials'
  }
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Build Docker Image') {
      steps { script { docker.build("${IMAGENAME}:${env.BUILD_NUMBER}") } }
    }
    stage('Push Docker Image') {
      steps {
        script {
          docker.withRegistry(REGISTRY, REGISTRYCREDENTIALS) {
            def tag = "${IMAGENAME}:${env.BUILD_NUMBER}"
            docker.image(tag).push()
            docker.image(tag).push("latest")
          }
        }
      }
    }
  }
}