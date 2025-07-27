FROM python:3.11-slim

WORKDIR /app

COPY pyjail.py .

EXPOSE 1337

CMD ["python3", "pyjail.py"]
