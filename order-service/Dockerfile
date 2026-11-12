FROM python:3.12-slim

WORKDIR /service
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY app ./app

ENV PORT=8000
EXPOSE 8000
CMD ["python", "-m", "app.main"]
