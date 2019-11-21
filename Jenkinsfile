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

    // all pipeline stages
    stages {
        stage('test') {
            steps {
                echo "Just test"
            }
        }
        stage('build') {
            steps {
                sh "docker build --tag portanizer_web ."
            }
        }
        stage('deploy') {
            steps {
                sh "docker stack deploy -c docker-compose-swarm.yml portanizer"
            }
            post {
                success {
                    sh "docker container prune"
                }
            }
        }
        stage('smoke-tests') {
            steps {
                // ensure the num of services is 3
                sh "docker ps -q | wc -l | grep 3"
            }
        }
    }
    post {
        always {
            cleanWs()
            sh "docker system prune"
        }
    }
}