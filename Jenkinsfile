pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                echo 'Creating isolated Python environment...'

                bat 'python -m venv .venv'

                echo 'Installing project dependencies...'

                bat '.venv\\Scripts\\python -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python -m pip install -r requirements.txt'
                bat '.venv\\Scripts\\python -m pip install pytest'
            }
        }

        stage('Run Tests') {
            steps {
                script {

                    echo 'Running automated tests...'

                    def testResult = bat(
                        returnStatus: true,
                        script: '.venv\\Scripts\\pytest -v > test_output.log 2>&1'
                    )

                    if (testResult != 0) {

                        echo 'Tests failed. Starting AI failure analysis...'

                        withCredentials([
                            string(
                                credentialsId: 'gemini-api-key',
                                variable: 'GEMINI_API_KEY'
                            )
                        ]) {

                            bat '.venv\\Scripts\\python ai_log_analyzer.py test_output.log'
                        }

                        archiveArtifacts(
                            artifacts: 'ai_failure_report.txt',
                            fingerprint: true
                        )

                        error 'Tests failed. AI failure analysis has been generated.'
                    }

                    echo 'All automated tests passed successfully.'
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'

                bat 'docker build -t ai-devops-demo:jenkins .'
            }
        }
    }

    post {

        success {
            echo '========================================'
            echo 'Pipeline completed successfully.'
            echo 'Tests passed and Docker image was built.'
            echo '========================================'
        }

        failure {
            echo '========================================'
            echo 'Pipeline failed.'
            echo 'AI-assisted failure analysis was performed.'
            echo '========================================'
        }
    }
}