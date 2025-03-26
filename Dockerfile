FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY supervisord.conf /app/supervisord.conf
COPY . .

CMD ["python", "app/main.py"]
