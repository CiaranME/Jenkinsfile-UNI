pipeline {
    agent any
    stages {
        stage('Clean Up') {
            steps {
                sh 'docker rm -f flask nginx || true'
                sh 'docker network rm app-network || true'
            }
        }
        stage('Set Up') {
            steps {
                sh 'docker network create app-network'
            }
        }
        stage('Build Images') {
            steps {
                sh 'docker build -t flask-app -f Dockerfile.flask .'
                sh 'docker build -t nginx-app -f Dockerfile.nginx .'
            }
        }
        stage('Run Containers') {
            steps {
                sh 'docker run -d --name flask --network app-network flask-app'
                sh 'docker run -d --name nginx --network app-network -p 80:80 nginx-app'
            }
        }
    }
}
