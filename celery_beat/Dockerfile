FROM python:3.11-slim

WORKDIR /magnetlinks

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["celery", "-A", "magnetlinks", "beat", "--loglevel=info", "--schedule=/var/lib/celery/celerybeat-schedule.db" ]
