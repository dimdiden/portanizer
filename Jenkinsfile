#!/usr/bin/env groovy

pipeline {
    agent {
        kubernetes {
            label 'kube-slave-python'
            defaultContainer 'python'
            slaveConnectTimeout 200
            yamlFile 'build.yaml'
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
        stage('Build-Push') {
            steps {
                container('docker') {
                    script {
                        def dockerImage = docker.build "${env.REGISTRY}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}"

                        docker.withRegistry('', env.DOCKER_HUB_CREDS) {
                            dockerImage.push()
                        }
                    }
                }
            }
        }
    }
}