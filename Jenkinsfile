// Main pipeline
pipeline {

    agent {
        node {
            label 'VD-build-box'
        }
    }

    options {
        ansiColor('xterm')
        parallelsAlwaysFailFast()
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    // all pipeline stages
    stages {
        stage('build') {
            steps {
                sh "docker-compose -f docker-compose-prod.yml build"
            }
        }
        stage('deploy') {
            steps {
                sh "docker-compose -f docker-compose-prod.yml down"
                sh "docker-compose -f docker-compose-prod.yml up -d"
            }
        }
        stage('smoke-tests') {
            steps {
                // ensure the num of services is 3
                sh "docker ps -q | wc -l | grep 3"
            }
        }
    }
}