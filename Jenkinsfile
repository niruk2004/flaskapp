pipeline {
    agent any
    environment {
        SONAR_TOKEN = credentials('sonarqube-token')
    }
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonarQubeServer') {
                    sh '''
                        # Optional: Download sonar-scanner if not available
                        if ! [ -x "$(command -v sonar-scanner)" ]; then
                          curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                          unzip sonar-scanner.zip
                          export PATH=$PATH:$(pwd)/sonar-scanner-*/bin
                        fi

                        sonar-scanner -Dsonar.login=${SONAR_TOKEN}
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