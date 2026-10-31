pipeline {
    agent any
    environment {
        AWS_PROFILE = 'default'
        AWS_REGION = 'us-east-1'
        ECR_REPO   = 'expenses-manager'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${ECR_REPO}:${IMAGE_TAG} ."
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    // Login to ECR using AWS CLI
                    sh "aws ecr get-login-password | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
                    sh "docker tag ${ECR_REPO}:${IMAGE_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"
                    sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}:${IMAGE_TAG}"
                }
            }
        }
        stage('Deploy via Terraform') {
            steps {
                script {
                    // Assume Terraform IaC for the target environment is in a sibling repo or submodule
                    // Here we just invoke a shared library step that runs "terraform apply" with the new image tag
                    jenkinsDeploy(environment: 'dev', imageTag: IMAGE_TAG)
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Deployment succeeded.'
        }
        failure {
            echo 'Deployment failed.'
        }
    }
}
