#!/usr/bin/env groovy

// Main pipeline
pipeline {

    agent {
        node {
            label 'VD-build-box'
        }
    }

    options {
        ansiColor('xterm')
        // parallelsAlwaysFailFast()
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        REGISTRY = credentials('portanizer-registry')
        DOCKER_HUB_CREDS = 'docker-hub-connector'
        DOMAIN = 'dedu.tk'
        POSTGRES_CREDS = credentials('portanizer-postgres-creds')
        POSTGRES_USER = "${POSTGRES_CREDS_USR}"
        POSTGRES_PASSWORD = "${POSTGRES_CREDS_PSW}"
        POSTGRES_DB = 'portanizer'
        DOCKER_IMAGE = ''
    }

    // all pipeline stages
    stages {
        stage('build&push') {
            when {
                anyOf {
                    branch 'master'
                    branch 'cicd'
                }
            }
            steps {
                script {
                    env.DOCKER_IMAGE = docker.build "${env.REGISTRY}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}"

                    docker.withRegistry( '', env.DOCKER_HUB_CREDS ) {
                        env.DOCKER_IMAGE.push()
                    }
                }
            }
        }
        stage('deploy') {
            when {
                branch 'master'
                branch 'cicd'
            }
            environment {
                IMAGE_TAG = "${env.REGISTRY}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'portanizer-env-file', variable: 'envFile')]) {
                        sh "cp ${envFile} ./.env"
                    }
                    sh "docker-compose -f docker-compose-prod.yml up -d"
                }
            }
        }
    }
    post {
        always {
            cleanWs()
            sh "docker rmi ${env.REGISTRY}:${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
        }
    }
}