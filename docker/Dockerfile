FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install numpy==1.24.3 scikit-learn==1.5.2
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY model.joblib .

EXPOSE 5000

CMD ["python", "src/deployment/app.py"]
