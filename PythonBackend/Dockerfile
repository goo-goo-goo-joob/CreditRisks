FROM snakepacker/python:all as builder

RUN python3.7 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U pip

COPY ./PythonBackend/requirements.txt /mnt/
RUN /usr/share/python3/app/bin/pip install -Ur /mnt/requirements.txt

FROM snakepacker/python:3.7 as api

COPY --from=builder /usr/share/python3/app /usr/share/python3/app
COPY ./PythonBackend .

CMD [ "/usr/share/python3/app/bin/python", "./server.py" ]
