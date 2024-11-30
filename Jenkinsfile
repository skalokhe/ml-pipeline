pipeline {
    agent any
    environment {
        GRAFANA_API_KEY = credentials('grafana-credentials')
        GRAFANA_URL = 'http://localhost:3000'
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
                    python3 -m pip install numpy>=1.26.0 pandas
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
        stage('Configure Grafana') {
            steps {
                script {
                    // Add Prometheus data source using basic auth
                    sh """
                        curl -X POST \
                        -u ${GRAFANA_CREDS_USR}:${GRAFANA_CREDS_PSW} \
                        -H 'Content-Type: application/json' \
                        ${GRAFANA_URL}/api/datasources \
                        -d '{
                            "name": "Prometheus",
                            "type": "prometheus",
                            "url": "http://prometheus:9090",
                            "access": "proxy",
                            "isDefault": true
                        }'
                    """
                    
                    // Deploy ML metrics dashboard using basic auth
                    sh """
                        curl -X POST \
                        -u ${GRAFANA_CREDS_USR}:${GRAFANA_CREDS_PSW} \
                        -H 'Content-Type: application/json' \
                        ${GRAFANA_URL}/api/dashboards/db \
                        -d '{
                            "dashboard": {
                                "id": null,
                                "title": "ML Model Metrics",
                                "panels": [
                                    {
                                        "title": "Model Prediction Latency",
                                        "type": "graph",
                                        "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0},
                                        "targets": [{
                                            "expr": "prediction_latency_seconds",
                                            "refId": "A"
                                        }]
                                    },
                                    {
                                        "title": "Prediction Requests Total",
                                        "type": "graph",
                                        "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0},
                                        "targets": [{
                                            "expr": "prediction_requests_total",
                                            "refId": "B"
                                        }]
                                    },
                                    {
                                        "title": "Model Accuracy",
                                        "type": "gauge",
                                        "gridPos": {"h": 8, "w": 8, "x": 0, "y": 8},
                                        "targets": [{
                                            "expr": "model_accuracy",
                                            "refId": "C"
                                        }]
                                    }
                                ]
                            },
                            "overwrite": true
                        }'
                    """
                }
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
        stage('Cleanup') {
            steps {
                cleanWs()
                sh 'docker system prune -af'
            }
        }
    }
}
