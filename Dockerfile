FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY app.py model.py ./
USER 10001:10001
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:create_app()"]
