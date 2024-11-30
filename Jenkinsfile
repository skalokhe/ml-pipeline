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
                    python -m venv venv
                    . venv/bin/activate
                    pip install pytest
                    pip install -r requirements.txt
                    python3 --version
                    pip3 --versio
                '''
                echo "completed installation of the dependencies"
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/ -v
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
    }
}
