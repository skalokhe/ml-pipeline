import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import numpy as np
from src.training.train_model import generate_data, train_model
from src.deployment.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_generate_data():
    X, y = generate_data()
    assert X.shape == (1000, 4)
    assert y.shape == (1000,)
    assert np.all((y == 0) | (y == 1))

def test_train_model():
    accuracy = train_model()
    assert 0 <= accuracy <= 1

def test_predict_endpoint(client):
    test_data = {"features": [0.1, 0.2, 0.3, 0.4]}
    response = client.post('/predict', json=test_data)
    assert response.status_code == 200
    assert 'prediction' in response.json
    assert isinstance(response.json['prediction'], int)
    assert response.json['prediction'] in [0, 1]