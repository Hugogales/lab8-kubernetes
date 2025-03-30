FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py service.py models.py ./
COPY templates ./templates
COPY static ./static

RUN mkdir -p /app/templates /app/static

EXPOSE 5000

CMD ["python", "-u", "app.py"] 