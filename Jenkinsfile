pipeline {
    agent any

    environment {
        DEPLOY_SERVER = "schmango-deploy"
        IMAGE_NAME = "schmango"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'http://10.74.74.72:3000/ax/Schmango.git'
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
                sh 'scp docker-compose.prod.yml ${DEPLOY_SERVER}:/opt/schmango/docker-compose.yml'
                sh 'scp -r nginx ${DEPLOY_SERVER}:/opt/schmango/'
                sh 'docker save ${IMAGE_NAME}:latest | ssh ${DEPLOY_SERVER} "docker load"'
                sh '''
                    ssh ${DEPLOY_SERVER} "cd /opt/schmango && \
                    sleep 10 && \
                    docker compose run --rm web python manage.py migrate && \
                    docker compose run --rm web python manage.py collectstatic --noinput && \
                    docker compose up -d"
                '''
            }
        }
    }
}