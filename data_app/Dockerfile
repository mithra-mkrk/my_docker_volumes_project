FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install --no-cache-dir Flask

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]