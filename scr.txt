node {
    stage('Clone Repository') {
        checkout scm
    }
    
    stage('Build Docker Image') {
        sh 'docker build -t flask-api .'
    }

    stage('Run Docker Container') {
        sh '''
        docker stop flask-api || true
        docker rm flask-api || true
        docker run -d -p 5000:5000 --name flask-api flask-api
        '''
    }
}