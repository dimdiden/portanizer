#!/usr/bin/env groovy

pipeline {
    agent {
        kubernetes {
            label 'kube-slave-docker'
            defaultContainer 'jnlp'
            slaveConnectTimeout 200
            yamlFile 'cicd/pod-docker.yml'
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
        REGISTRY = "dimdiden/kubectl-arm"
        DOCKER_HUB_CREDS = 'docker-hub-connector'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/dimdiden/portanizer.git'
            }
        }
        stage('Build-Push') {
            steps {
                container('docker') {
                    script {
                        dir('cicd') {
                            def dockerImage = docker.build "${env.REGISTRY}"

                            docker.withRegistry('', env.DOCKER_HUB_CREDS) {
                                dockerImage.push()
                            }
                        }
                    }
                }
            }
        }
    }
}