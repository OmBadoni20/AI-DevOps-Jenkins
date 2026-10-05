pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                script {

                    def testResult = bat(
                        returnStatus: true,
                        script: 'pytest -v > test_output.log 2>&1'
                    )

                    bat 'type test_output.log'

                    if (testResult != 0) {

                        echo 'Tests failed. Starting AI failure analysis...'

                        withCredentials([
                            string(
                                credentialsId: 'gemini-api-key',
                                variable: 'GEMINI_API_KEY'
                            )
                        ]) {
                            bat 'python ai_log_analyzer.py test_output.log'
                        }

                        archiveArtifacts(
                            artifacts: 'ai_failure_report.txt',
                            fingerprint: true
                        )

                        error 'Tests failed. AI failure analysis has been generated.'
                    }
                }
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
            echo 'Pipeline failed. AI-assisted failure analysis was performed.'
        }
    }
}