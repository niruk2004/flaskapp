pipeline {
    agent any
stages {
        stage('Clone Repository') {
            steps {
                git url: '<your-repo-url>', branch: 'main'
            }
        }
stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-api .'
            }
        }
stage('Run Docker Container') {
            steps {
                sh '''
                docker stop flask-api || true
                docker rm flask-api || true
                docker run -d -p 5000:5000 --name flask-api flask-api
                '''
            }
        }
    }
}