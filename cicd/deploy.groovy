#!/usr/bin/env groovy

pipeline {
    agent {
        kubernetes {
            label 'kube-slave-kubectl'
            defaultContainer 'jnlp'
            slaveConnectTimeout 200
            yamlFile 'cicd/pod-kubelet.yml'
        }
    }

    options {
        ansiColor('xterm')
        timestamps()
        skipDefaultCheckout()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    parameters {
        string(name: 'VERSION', defaultValue: 'latest', description: 'Version of the docker image')
    }

    stages {
        stage('Checkout') {
            steps {
                git url: 'https://github.com/dimdiden/portanizer.git'
            }
        }
        stage('Deploy') {
            steps {
                container('kubectl') {
                    script {
                        sh "ls -la"
                        sh "kubectl apply -f cicd/kubernetes"
                    }
                }
            }
        }
    }
}