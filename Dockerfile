FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app_api.py .
COPY src/ ./src/
COPY models/sentiment_pipeline.joblib ./models/sentiment_pipeline.joblib

EXPOSE 7860

CMD ["uvicorn", "app_api:app", "--host", "0.0.0.0", "--port", "7860"]
