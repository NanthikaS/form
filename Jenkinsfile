pipeline {
    agent any

    environment {
        FLASK_ENV = 'production'
        DOCKER_IMAGE = 'your-dockerhub-username/flask-app'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials' // Replace with your Jenkins credentials ID for Docker Hub
    }

    stages {
        stage('Checkout') {
            steps {
                // Clone the Git repository
                git url: 'https://github.com/your-username/your-repo.git', branch: 'main'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install Python dependencies
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Application') {
            steps {
                // Run Flask application
                sh 'python3 app.py &'
                sleep 10 // Allow some time for the app to start
            }
        }

        stage('Test Application') {
            steps {
                // Here, you can add any tests you want to run. For now, we'll just check if the app is running.
                script {
                    def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:5000", returnStdout: true).trim()
                    if (response != '200') {
                        error('Flask app did not start successfully.')
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the Docker image
                    dockerImage = docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    // Log in to Docker Hub and push the image
                    docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                        dockerImage.push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                // Assuming you have a Kubernetes deployment file or use Helm
                sh 'kubectl apply -f k8s/deployment.yaml' // Replace with your actual deployment command
            }
        }
    }

    post {
        always {
            // Clean up after build
            cleanWs()
        }
        success {
            // Actions on successful build
            echo 'Build succeeded!'
        }
        failure {
            // Actions on failed build
            echo 'Build failed!'
        }
    }
}
