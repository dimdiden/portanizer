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
                        env.version = sh(
                            script: 'grep current_version .bumpversion.cfg | sed -e s/"^.*= "//',
                            returnStdout: true
                        ).trim()
                        def dockerImage = docker.build "${env.REGISTRY}:${env.version}"

                        docker.withRegistry('', env.DOCKER_HUB_CREDS) {
                            dockerImage.push()
                            dockerImage.push('latest')
                        }
                        
                        currentBuild.displayName = "${env.version}-#${env.BUILD_NUMBER}"
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
                    string(name: 'VERSION', value: env.version)
                ]
            }
        }
    }
}