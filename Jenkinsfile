pipeline {
    agent any

    environment {
        KUBECONFIG_FILE = 'kubeconfig' 
    }

    stages {
        stage("Cleanup") {
            steps {
                sh 'docker rm -f $(docker ps -a -q --filter "label=app=ibrahim161616") || true'
                sh 'docker rmi -f $(docker images -q --filter "label=app=ibrahim161616") || true'
            }
        }
        stage("Build Docker Image") {
            steps {
                sh 'docker build -t ibrahim161616/activity4:app -f Dockerfile .'
            }
        }
        stage("Push Image to Docker Hub") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                    docker push ibrahim161616/activity4:app
                    '''
                }
            }
        }

        stage("Orchestrate Containers on Kubernetes") {
            steps {
                withCredentials([file(credentialsId: "${env.KUBECONFIG_FILE}", variable: 'KUBECONFIG')]) {
                    sh '''
                    kubectl apply -f flask_deployment.yaml
                    kubectl apply -f flask_service.yaml
                    kubectl apply -f nginx_deployment.yaml
                    kubectl apply -f nginx_service.yaml
                    '''
                }
            } 
        }
    }
}
