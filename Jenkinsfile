pipeline {
    agent any

    environment {
        SONAR_TOKEN = credentials('sonarqube-token')
        DOCKER_CREDENTIALS = credentials('niruk2004-dockerhub')
        IMAGE_NAME = "niruk2004/flask-api:latest"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
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
                        curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                        unzip -o -q sonar-scanner.zip
                        ./sonar-scanner-*/bin/sonar-scanner -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh '''
                    docker stop flask-api || true
                    docker rm flask-api || true
                    docker run -d -p 5000:5000 --name flask-api ${IMAGE_NAME}
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                sh '''
                    echo "${DOCKER_CREDENTIALS_PSW}" | docker login -u "${DOCKER_CREDENTIALS_USR}" --password-stdin
                    docker push ${IMAGE_NAME}
                    docker logout
                '''
            }
        }
    }
}
