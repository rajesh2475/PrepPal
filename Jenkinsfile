pipeline {
    agent any

    environment {
        // Define environment variables
        DOCKER_IMAGE = "hub.docker.com/preppal-app:latest"
        SONARQUBE_SERVER = "SonarQubeServer" // Name of the SonarQube server configured in Jenkins
        EMAIL_RECIPIENTS = "rajesh@gmail.com"
    }

    stages {
        stage('Clone Code') {
            steps {
                echo "Cloning the repository..."
                checkout scm
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo "Running unit tests..."
                sh 'python3 -m unittest discover -s tests/unittests'
            }
        }

        stage('Send Unit Test Results to SonarQube') {
            steps {
                echo "Sending unit test results to SonarQube..."
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh 'sonar-scanner -Dsonar.projectKey=PrepPal -Dsonar.sources=app -Dsonar.tests=tests/unittests -Dsonar.python.xunit.reportPath=unittest-results.xml'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh 'docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Push Docker Image to Registry') {
            steps {
                echo "Pushing Docker image to registry..."
                sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
                sh 'docker push ${DOCKER_IMAGE}'
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded. Sending success email..."
            mail to: "${EMAIL_RECIPIENTS}",
                 subject: "Jenkins Pipeline Success: PrepPal",
                 body: "The Jenkins pipeline for PrepPal completed successfully."
        }
        failure {
            echo "Pipeline failed. Sending failure email..."
            mail to: "${EMAIL_RECIPIENTS}",
                 subject: "Jenkins Pipeline Failure: PrepPal",
                 body: "The Jenkins pipeline for PrepPal failed. Please check the Jenkins logs for details."
        }
    }
}