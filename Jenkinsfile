pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker run --rm \
                      --user "$(id -u):$(id -g)" \
                      --env HOME=/tmp \
                      --volume "$WORKSPACE:/workspace" \
                      --workdir /workspace \
                      python:3.12-slim \
                      sh -c "
                        python -m pip install \
                          --user \
                          --no-cache-dir \
                          -r requirements.txt \
                          -r requirements-dev.txt &&
                        python -m pytest -v
                      "
                '''
            }
        }

        stage('Validate Compose') {
            environment {
                SECRET_KEY = 'jenkins-validation-placeholder'
            }
            steps {
                sh 'docker compose config --quiet'
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                    docker build \
                      --tag "opstrack:jenkins-${BUILD_NUMBER}" \
                      .
                '''
            }
        }
    }

    post {
        success {
            echo 'OpsTrack Jenkins pipeline completed successfully!'
        }

        failure {
            echo 'OpsTrack Jenkins pipeline failed. Check the failed stage logs.'
        }

        always {
            sh '''
                docker image rm \
                  "opstrack:jenkins-${BUILD_NUMBER}" \
                  2>/dev/null || true
            '''
        }
    }
}
