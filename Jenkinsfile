pipeline {
    agent any

    parameters {
        choice(
            name: 'JOB_TYPE',
            choices: ['BUILD_AND_PUSH', 'DEPLOY', 'ALL'],
            description: 'Choose task: Build & Push Docker image, Deploy to AWS, or Both'
        )
        string(
            name: 'AWS_ACCOUNT_ID',
            defaultValue: '250326384271',
            description: 'AWS Account ID'
        )
        string(
            name: 'AWS_REGION',
            defaultValue: 'us-east-1',
            description: 'AWS Region'
        )
        string(
            name: 'ECR_REPO_NAME',
            defaultValue: 'expenses-manager',
            description: 'ECR Repository Name'
        )
        string(
            name: 'IMAGE_TAG',
            defaultValue: '',
            description: 'Docker image tag (defaults to build number if empty)'
        )
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'prod'],
            description: 'Target deployment environment'
        )
    }

    environment {
        AWS_DEFAULT_REGION = "${params.AWS_REGION}"
        TAG                = "${params.IMAGE_TAG != '' ? params.IMAGE_TAG : env.BUILD_NUMBER}"
        ECR_URI            = "${params.AWS_ACCOUNT_ID}.dkr.ecr.${params.AWS_REGION}.amazonaws.com/${params.ECR_REPO_NAME}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        // ==========================================
        // JOB 1: DOCKER BUILD & PUSH TO ECR
        // ==========================================
        stage('Docker Build') {
            when {
                expression { params.JOB_TYPE == 'BUILD_AND_PUSH' || params.JOB_TYPE == 'ALL' }
            }
            steps {
                echo "Building Docker image: ${ECR_URI}:${TAG}"
                sh "docker build -t ${ECR_URI}:${TAG} -t ${ECR_URI}:latest ."
            }
        }

        stage('Push to ECR') {
            when {
                expression { params.JOB_TYPE == 'BUILD_AND_PUSH' || params.JOB_TYPE == 'ALL' }
            }
            steps {
                echo "Authenticating with Amazon ECR..."
                sh """
                    aws ecr get-login-password --region ${params.AWS_REGION} | \
                      docker login --username AWS --password-stdin ${params.AWS_ACCOUNT_ID}.dkr.ecr.${params.AWS_REGION}.amazonaws.com
                    
                    echo "Pushing image tags..."
                    docker push ${ECR_URI}:${TAG}
                    docker push ${ECR_URI}:latest
                """
            }
        }

        // ==========================================
        // JOB 2: DEPLOY CODE TO AWS
        // ==========================================
        stage('Deploy to AWS') {
            when {
                expression { params.JOB_TYPE == 'DEPLOY' || params.JOB_TYPE == 'ALL' }
            }
            steps {
                echo "Deploying image ${ECR_URI}:${TAG} to ${params.ENVIRONMENT} environment..."
                script {
                    // Check if infra folder is available as sibling directory
                    def infraDir = "../infra/environments/${params.ENVIRONMENT}"
                    if (fileExists(infraDir)) {
                        dir(infraDir) {
                            sh """
                                terraform init
                                terraform apply -auto-approve -var="image_tag=${TAG}"
                            """
                        }
                    } else {
                        echo "Infra path ${infraDir} not found in workspace workspace root."
                        echo "Simulating application rollout for image: ${ECR_URI}:${TAG} on ${params.ENVIRONMENT}"
                        // If using ECS / App runner / EC2:
                        // sh "aws ecs update-service --cluster ... --service ... --force-new-deployment"
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
        success {
            echo "Pipeline finished successfully!"
        }
        failure {
            echo "Pipeline encountered an error. Check console output."
        }
    }
}
