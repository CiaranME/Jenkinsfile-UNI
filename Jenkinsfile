pipeline {
    agent any
    stages {
        stage('Clean Up') {
            steps {
                sh 'docker rm -f flask nginx || true'
                sh 'docker network rm app-network || true'
            }
        }
        stage('Trivy FS Scan') {
            steps {
                sh 'trivy fs --format table -o trivy-fs-report.txt .'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-fs-report.txt'
                }
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
        stage('Trivy Image Scan') {
            steps {
                sh 'trivy image --format table -o trivy-image-report.txt flask-app'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-image-report.txt'
                }
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
