pipeline {
    agent any

    stages {
        stage('Build and Deploy') {
            steps {
                script {
                    // Execute docker-compose command with the provided environment file
                    sh 'docker-compose --env-file ./config/.env.stg up --build -d'
                }
            }
        }

        stage('Remove unused images') {
            steps {
                script {
                    // Remove unused Docker images
                    sh 'docker image prune -a -f'
                }
            }
        }
    }
}
