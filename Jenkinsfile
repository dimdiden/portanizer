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
                        version = sh(
                            script: 'grep current_version .bumpversion.cfg | sed -e s/"^.*= "//',
                            returnStdout: true
                        ).trim()
                        def dockerImage = docker.build "${env.REGISTRY}:${version}"

                        docker.withRegistry('', env.DOCKER_HUB_CREDS) {
                            dockerImage.push()
                            dockerImage.push('latest')
                        }
                        gitHash = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
                        
                        currentBuild.displayName = "${version}-${gitHash}-#${env.BUILD_NUMBER}"
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