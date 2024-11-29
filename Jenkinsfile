pipeline {
    agent any
    
    stages {
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
