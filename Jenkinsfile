pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        DOCKERHUB_IMAGE = 'wkavindu/opstrack'
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
                      --tag "${DOCKERHUB_IMAGE}:jenkins-${BUILD_NUMBER}" \
                      .
                '''
            }
        }

        stage('Push Image') {
            when {
                expression {
                    env.GIT_BRANCH == 'origin/main'
                }
            }

            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USERNAME',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x

                        echo "$DOCKERHUB_TOKEN" |
                          docker login \
                            --username "$DOCKERHUB_USERNAME" \
                            --password-stdin

                        docker push \
                          "${DOCKERHUB_IMAGE}:jenkins-${BUILD_NUMBER}"

                        docker tag \
                          "${DOCKERHUB_IMAGE}:jenkins-${BUILD_NUMBER}" \
                          "${DOCKERHUB_IMAGE}:jenkins-latest"

                        docker push \
                          "${DOCKERHUB_IMAGE}:jenkins-latest"

                        docker logout
                    '''
                }
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
                  "${DOCKERHUB_IMAGE}:jenkins-${BUILD_NUMBER}" \
                  "${DOCKERHUB_IMAGE}:jenkins-latest" \
                  2>/dev/null || true
            '''
        }
    }
}