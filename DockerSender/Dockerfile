FROM python:3

WORKDIR /app

COPY sender.py /app/
COPY pila.txt /app/

RUN pip install socketio pickle-mixin

CMD ["python", "sender.py"]