pipeline {
    agent any
    environment {
        SONAR_TOKEN = credentials('sonarqube-token')
    }
    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir() // Deletes all files in the workspace before proceeding
            }
        }

        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonarQubeServer') {
                    sh '''
                        # Download and unzip sonar-scanner
                        curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                        unzip -o -q sonar-scanner.zip

                        # Set path to sonar-scanner binary using absolute path
                        ./sonar-scanner-*/bin/sonar-scanner -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
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