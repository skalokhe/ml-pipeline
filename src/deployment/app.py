from flask import Flask, request, jsonify
import joblib
import numpy as np
from prometheus_client import Counter, generate_latest

app = Flask(__name__)
model = joblib.load('model.joblib')

PREDICTIONS = Counter('predictions_total', 'Total number of predictions made')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict(np.array(data['features']).reshape(1, -1))
    PREDICTIONS.inc()
    return jsonify({'prediction': int(prediction[0])})

@app.route('/metrics')
def metrics():
    return generate_latest()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
