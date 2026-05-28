pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'echo "Building..."'
                sh 'touch build.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'echo "Testing..."'
                sh 'ls -la'
            }
        }
        stage('Deploy') {
            steps {
                sh 'echo "Deploying..."'
                sh 'pwd'
                sh 'mv build.txt deployed.txt'
            }
        }
    }
}
