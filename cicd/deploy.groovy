#!/usr/bin/env groovy

pipeline {
    agent {
        kubernetes {
            label 'kube-slave-kubectl'
            defaultContainer 'kubectl'
            slaveConnectTimeout 200
            yamlFile 'cicd/build.yml'
        }
    }

    options {
        ansiColor('xterm')
        // parallelsAlwaysFailFast()
        timestamps()
        skipDefaultCheckout()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    // environment {
    //     KUBECONFIG = credentials('kube-config')
    // }

    stages {
        // stage('Checkout') {
        //     steps {
        //         git 'https://github.com/dimdiden/portanizer.git'
        //     }
        // }
        stage('Deploy') {
            steps {
                container('kubectl') {
                    script {
                        sh "kubectl apply -f cicd/kubernetes"
                    }
                }
            }
        }
    }
}