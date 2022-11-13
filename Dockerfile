# base image
FROM python:3.10

RUN apt-get update && apt-get install -y locales

RUN mkdir /service
COPY . /service/
WORKDIR /service

RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

# run the application
ENTRYPOINT ["python", "main.py"]
