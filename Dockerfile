FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV ENVIRONMENT=local

WORKDIR /app

COPY requirements/local.txt local-requirements.txt
RUN pip install --no-cache-dir -r local-requirements.txt && rm local-requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
