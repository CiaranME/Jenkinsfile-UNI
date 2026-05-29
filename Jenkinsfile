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
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh 'trivy fs --exit-code 1 --severity CRITICAL --format json -o trivy-fs-report.json .'
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-fs-report.json'
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
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh 'trivy image --exit-code 1 --severity CRITICAL --format json -o trivy-image-report.json flask-app'
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-image-report.json'
                }
            }
        }
        stage('Run Containers') {
            steps {
                sh 'docker run -d --name flask --network app-network flask-app'
                sh 'docker run -d --name nginx --network app-network -p 80:80 nginx-app'
            }
        }
        stage('Unit Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh 'python3 test_app.py'
                }
            }
        }
    }
}
