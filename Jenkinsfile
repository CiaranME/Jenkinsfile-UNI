pipeline {
    agent any
    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-credentials')
        IMAGE_NAME = 'ciaranme/flask-app'
        IMAGE_TAG = "build-${BUILD_NUMBER}"
    }
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
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -f Dockerfile.flask .'
                sh 'docker build -t nginx-app -f Dockerfile.nginx .'
            }
        }
        stage('Trivy Image Scan') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    sh 'trivy image --exit-code 1 --severity CRITICAL --format json -o trivy-image-report.json ${IMAGE_NAME}:${IMAGE_TAG}'
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-image-report.json'
                }
            }
        }
        stage('Approval') {
            steps {
                input message: 'Scans complete. Review results and approve to deploy?', ok: 'Deploy'
            }
        }
        stage('Push to DockerHub') {
            steps {
                sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                sh 'docker push ${IMAGE_NAME}:${IMAGE_TAG}'
            }
        }
        stage('Run Containers') {
            steps {
                sh 'docker run -d --name flask --network app-network ${IMAGE_NAME}:${IMAGE_TAG}'
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
       stage('Generate Metadata') {
    steps {
        sh """
            cat > build-metadata.json << EOF
{
  "buildNumber": "${BUILD_NUMBER}",
  "gitCommit": "${GIT_COMMIT}",
  "imageName": "${IMAGE_NAME}",
  "imageTag": "${IMAGE_TAG}",
  "buildTime": "\$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
        """
        archiveArtifacts artifacts: 'build-metadata.json'
    }
}
        stage('Generate SBOM') {
            steps {
                sh 'trivy image --format cyclonedx -o sbom.json ${IMAGE_NAME}:${IMAGE_TAG}'
                archiveArtifacts artifacts: 'sbom.json'
            }
        }
    }
}
