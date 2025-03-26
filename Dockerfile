FROM python:3.12

#Docker compose
ENV PYTHONUNBUFFERED=1

WORKDIR /budget-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
