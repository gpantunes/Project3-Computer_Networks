#Author Guilherme Antunes nº 62621
#Author Rodrigo Loução nº 63627

FROM python:3

WORKDIR /app

COPY sender.py /app/
COPY file1.txt /app/

RUN pip install socketio pickle-mixin

CMD ["python", "sender.py", "172.17.0.3", "20001", "172.17.0.2", "54321", "file1.txt", "4"]