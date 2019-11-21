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
        DOMAIN = 'dedu.tk'
        POSTGRES_CREDS = credentials('portanizer-postgres-creds')
        POSTGRES_USER = "${POSTGRES_CREDS_USR}"
        POSTGRES_PASSWORD = "${POSTGRES_CREDS_PSW}"
        POSTGRES_DB = 'portanizer'
    }

    // all pipeline stages
    stages {
        stage('build') {
            steps {
                sh "docker build --tag portanizer_web ."
            }
        }
        stage('deploy') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'portanizer-env-file', variable: 'envFile')]) {
                        sh "cp ${envFile} .env"
                    }
                    sh "docker stack deploy -c docker-compose-swarm.yml portanizer"
                }
            }
            post {
                success {
                    sh "docker container prune"
                }
            }
        }
        // stage('smoke-tests') {
        //     steps {
        //         // ensure the num of services is 3
        //         sh "docker ps -q | wc -l | grep 3"
        //     }
        // }
    }
    post {
        always {
            cleanWs()
            sh "docker system prune"
        }
    }
}