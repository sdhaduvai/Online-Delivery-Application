FROM python:3.7

WORKDIR /app

COPY . /app

RUN apt install -y netcat

RUN pip install -r requirements.txt

EXPOSE 7006

CMD python buyer.py