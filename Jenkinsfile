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
        REGISTRY = "dimdiden/portanizer-arm"
        DOCKER_HUB_CREDS = 'docker-hub-connector'
        VERSION = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/dimdiden/portanizer.git'
            }
        }
        stage('Build-Push') {
            when {
                anyOf {
                    branch 'master'
                }
            }
            steps {
                container('docker') {
                    script {
                        def dockerImage = docker.build "${env.REGISTRY}:${VERSION}"

                        docker.withRegistry('', env.DOCKER_HUB_CREDS) {
                            dockerImage.push()
                        }
                    }
                }
            }
        }
        stage('Deploy') {
            when {
                anyOf {
                    branch 'master'
                }
            }
            steps {
                build job: 'portanizer/portanizer-deploy', wait: true, parameters: [
                    string(name: 'VERSION', value: VERSION)
                ]
            }
        }
    }
}