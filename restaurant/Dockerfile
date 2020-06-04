FROM python:3.7

WORKDIR /app

COPY . /app

RUN apt install -y netcat

RUN pip install -r requirements.txt

CMD python restaurant.py