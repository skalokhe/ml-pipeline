pipeline {
    agent any
    
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
                    python3 -m pip install --upgrade "pip<24.0" "setuptools<69.0" wheel
                    python3 -m pip install --no-build-isolation numpy==1.24.3
                    python3 -m pip install --no-build-isolation pytest scikit-learn==1.3.2 flask joblib prometheus_client
                    python3 -m pip install -r requirements.txt
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
        stage('Test'){
            steps{
                sh 'pytest'
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
        
        stage('Train') {
            steps {
                sh '''
                    . venv/bin/activate
                    python src/training/train_model.py
                '''
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker-compose -f docker/docker-compose.yml up -d'
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
