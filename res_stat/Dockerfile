FROM python:3.7

WORKDIR /app

COPY . /app

RUN apt install -y netcat

RUN pip install -r requirements.txt

EXPOSE 7007

CMD python restaurant_status.py