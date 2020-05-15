#!/usr/bin/env groovy

pipeline {
    agent {
        kubernetes {
            label 'kube-slave-python'
            defaultContainer 'python'
            yaml """
apiVersion: "v1"
kind: "Pod"
metadata:
  labels:
    label: "kube-slave-python"
spec:
  containers:
  - name: "python"
    image: "arm64v8/python"
    command: ['cat']
    tty: true
    workingDir: "/home/jenkins/agent"
  - name: "jnlp"
    image: "dimdiden/jenkins-slave:jdk11"
    tty: true
    workingDir: "/home/jenkins/agent"
  - name: docker
    image: docker:latest
    command: ['cat']
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
"""
        }
    }

    options {
        ansiColor('xterm')
        // parallelsAlwaysFailFast()
        timestamps()
        skipDefaultCheckout()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        REGISTRY = credentials('portanizer-registry')
        DOCKER_HUB_CREDS = 'docker-hub-connector'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/dimdiden/portanizer.git'
            }
        }
        stage('Build-Image') {
            steps {
                container('docker') {
                    script {
                        def dockerImage = docker.build "${env.REGISTRY}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}"

                        docker.withRegistry( '', env.DOCKER_HUB_CREDS ) {
                            dockerImage.push()
                        }
                    }
                }
            }
        }
    }
}