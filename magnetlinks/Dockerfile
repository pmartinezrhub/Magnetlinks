FROM python:3.11

WORKDIR /magnetlinks

COPY requirements.txt /magnetlinks/
RUN pip install --no-cache-dir -r requirements.txt

COPY magnetlinks/ /magnetlinks/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


