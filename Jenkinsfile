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
                    which python3
                    python3 -m venv venv
                    . venv/bin/activate
                    python3 -m pip install --upgrade pip
                    python3 -m pip install numpy==1.24.3
                    python3 -m pip install pytest
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
