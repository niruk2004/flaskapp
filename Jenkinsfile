node {
    stage('Clean Workspace') {
        deleteDir() // Deletes all files in the workspace before proceeding
    }

    stage('Clone Repository') {
        checkout scm
    }

    stage('Build Docker Image') {
        sh 'docker build -t flask-api .'
    }

    stage('SonarQube Analysis') {
        withSonarQubeEnv('MySonarQubeServer') {
            withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
                sh '''
                    # Download and unzip sonar-scanner
                    curl -sSLo sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
                    unzip -o -q sonar-scanner.zip

                    # Run Sonar analysis
                    ./sonar-scanner-*/bin/sonar-scanner -Dsonar.login=${SONAR_TOKEN}
                '''
            }
        }
    }

    stage('Download Sonar Report') {
        withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
            sh '''
            #in the 172.18.0.3, it is ur ip in the network or the bridge adapter that you are using
                curl -u "${SONAR_TOKEN}:" \
                  "http://172.17.0.3:9000/api/measures/component?component=flaskapp&metricKeys=bugs,vulnerabilities,code_smells" \
                  -o sonar-report.json
            '''
        }
    }

    stage('Run Docker Container') {
        sh '''
        docker stop flask-api || true
        docker rm flask-api || true
        docker run -d -p 5000:5000 --name flask-api flask-api
        '''
    }

    // Post actions: Archive report
     stage('Archive Sonar Report') {
        archiveArtifacts artifacts: 'sonar-report.json', fingerprint: true
    }
}
