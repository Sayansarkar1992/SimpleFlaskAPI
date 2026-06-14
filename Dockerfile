FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt .
RUN apk add --no-cache curl
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 5000

CMD ["python", "app.py"]