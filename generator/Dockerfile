FROM python:3.11-slim

WORKDIR /app
COPY app.py .

RUN pip install --no-cache-dir fastapi uvicorn pydantic

EXPOSE 8002

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8002"]