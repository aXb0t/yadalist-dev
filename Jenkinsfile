pipeline {
    agent any

    parameters {
        choice(
            name: 'DEPLOY_ENV',
            choices: ['homelab', 'production'],
            description: 'Select deployment environment'
        )
    }

    environment {
        IMAGE_NAME = "schmango"
        IMAGE_TAG = "${BUILD_NUMBER}"
        // Set deploy server based on environment parameter
        DEPLOY_SERVER = "${params.DEPLOY_ENV == 'production' ? 'schmango-prod' : 'schmango-deploy'}"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'http://10.74.74.72:3000/ax/Schmango.git'
            }
        }

        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'npm ci'
                    sh 'npm run build'
                    sh 'npm run build-storybook'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
                sh 'docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest'
            }
        }

        stage('Test') {
            steps {
                sh 'docker run --rm -e DJANGO_SETTINGS_MODULE=schmango.settings.testing ${IMAGE_NAME}:${IMAGE_TAG} python manage.py test'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Deploying to ${params.DEPLOY_ENV} environment..."

                    // Select nginx config based on environment
                    def nginxConfig = params.DEPLOY_ENV == 'production' ? 'nginx.production.conf' : 'nginx.testing.conf'

                    // Copy environment-specific nginx config
                    sh "scp nginx/${nginxConfig} ${DEPLOY_SERVER}:/opt/schmango/nginx/nginx.conf"

                    // Copy Storybook static files to deployment server
                    sh "ssh ${DEPLOY_SERVER} 'mkdir -p /opt/schmango/storybook'"
                    sh "scp -r frontend/storybook-static/* ${DEPLOY_SERVER}:/opt/schmango/storybook/"

                    // Copy scripts directory
                    sh "ssh ${DEPLOY_SERVER} 'mkdir -p /opt/schmango/scripts'"
                    sh "scp scripts/* ${DEPLOY_SERVER}:/opt/schmango/scripts/"
                    sh "ssh ${DEPLOY_SERVER} 'chmod +x /opt/schmango/scripts/*.sh'"
                }
                sh 'scp docker-compose.prod.yml ${DEPLOY_SERVER}:/opt/schmango/docker-compose.yml'
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