FROM python:3

WORKDIR /app

COPY reciever.py /app/

RUN pip install socketio pickle-mixin

CMD ["python", "reciever.py", "172.17.0.2", "54321", "untitled0.txt"]