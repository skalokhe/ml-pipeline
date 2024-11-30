pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = "your-registry"
        IMAGE_NAME = "ml-service"
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS = credentials('docker-cred-id')
        KUBECONFIG = credentials('kubeconfig-id')
    }
    stages {
        stage('checkout'){
            steps {

            echo "git clone is complete"
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    python3 -m pip install --upgrade pip setuptools wheel
                    python3 -m pip install Cython
                    python3 -m pip install numpy>=1.26.0
                    python3 -m pip install pytest scikit-learn==1.3.2 flask joblib prometheus_client
                    python3 --version
                    pip --version
                '''
                echo "completed installation of the dependencies"
            }
        }
        stage('Train Model') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 src/training/train_model.py
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 -m pytest tests/ -v
                '''
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose -f docker/docker-compose.yml up -d'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} -f docker/Dockerfile ."
            }
        }
        
        stage('Push Docker Image') {
            steps {
                sh '''
                    echo $DOCKER_CREDENTIALS_PSW | docker login $DOCKER_REGISTRY -u $DOCKER_CREDENTIALS_USR --password-stdin
                    docker push ${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl --kubeconfig=$KUBECONFIG apply -f k8s/deployment.yaml
                    kubectl --kubeconfig=$KUBECONFIG set image deployment/ml-service ml-service=${DOCKER_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
        stage('Cleanup') {
            steps {
                cleanWs()
                sh 'docker system prune -af'
            }
        }
    }
}
