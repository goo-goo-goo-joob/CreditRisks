FROM python:3.7.5-slim
WORKDIR /usr/src/app

COPY ./PythonBackend .
RUN apt-get update && apt-get -qq -y install curl && apt-get -qq -y install python3-dev openssl-dev libffi-dev gcc
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt --no-binary grpcio

CMD [ "python", "./server.py" ]