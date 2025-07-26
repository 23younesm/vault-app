FROM python:3.11-slim

WORKDIR /app
COPY app.py vault.db ./ 
COPY static/ static/

RUN pip install flask

ENV FLASK_ENV=production

CMD ["python", "app.py"]
