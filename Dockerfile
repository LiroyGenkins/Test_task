# base image
FROM python:3.10.0-slim

RUN apt-get update && apt-get install -y locales

RUN mkdir /service
COPY . /service/
WORKDIR /service

RUN python -m venv venv
RUN  python3.10 -m pip install --upgrade pip
RUN  python3.10 -m pip install -r requirements.txt

# run the application
EXPOSE 8000

ENTRYPOINT ["python", "main.py"]
