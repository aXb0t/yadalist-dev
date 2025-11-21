pipeline {
    agent any

    environment {
        IMAGE_NAME = "myapp"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'http://10.74.74.72:3000/ax/DockerDjango.git'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                sh 'docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python manage.py test'
            }
        }

        stage('Deploy to Homelab') {
            steps {
                sh '''
                    # Copy docker-compose.yml to deployment server
                    scp docker-compose.yml containers:/opt/myapp/

                    # Save the built image and transfer it
                    docker save ${IMAGE_NAME}:latest | ssh containers "docker load"

                    ssh containers "cd /opt/myapp && \
                    docker-compose pull && \
                    docker-compose run --rm web python manage.py migrate && \
                    docker-compose up -d"
                '''
            }
        }
    }
}