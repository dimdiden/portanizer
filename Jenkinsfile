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
    command:
    - "cat"
    image: "arm64v8/python"
    imagePullPolicy: "IfNotPresent"
    tty: true
    workingDir: "/home/jenkins/agent"
  - name: "jnlp"
    image: "dimdiden/jenkins-slave:jdk11"
    tty: true
    workingDir: "/home/jenkins/agent"
"""
        }
    }

    options {
        ansiColor('xterm')
        // parallelsAlwaysFailFast()
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                sh "ls -la"
            }
        }
    }
}