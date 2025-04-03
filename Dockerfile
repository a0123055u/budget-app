FROM python:3.12

#Docker compose
ENV PYTHONUNBUFFERED=1

WORKDIR /budget-app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

RUN chmod +x /budget-app/entrypoint.sh
ENTRYPOINT ["/budget-app/entrypoint.sh"]