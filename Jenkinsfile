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
            when {
                branch 'master'
            }
            steps {
                sh "docker build --tag portanizer_web ."
            }
        }
        stage('deploy') {
            when {
                branch 'master'
            }
            steps {
                script {
                    withCredentials([file(credentialsId: 'portanizer-env-file', variable: 'envFile')]) {
                        sh "cp ${envFile} .env"
                    }
                    sh "docker stack deploy -c docker-compose-swarm.yml portanizer"
                }
            }
        }
    }
    post {
        always {
            cleanWs()
            sh "docker system prune -f"
        }
    }
}