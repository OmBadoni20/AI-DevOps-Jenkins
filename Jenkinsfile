pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m pip install pytest'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'pytest -v'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t ai-devops-demo:jenkins .'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Manual log analysis is required.'
        }
    }
}