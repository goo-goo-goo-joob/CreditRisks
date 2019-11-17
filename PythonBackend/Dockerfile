FROM python:3.7.5-slim
WORKDIR /usr/src/app

COPY ./PythonBackend .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./server.py" ]