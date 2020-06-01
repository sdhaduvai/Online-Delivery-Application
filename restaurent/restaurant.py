from flask import Flask, jsonify, request, abort, make_response
from kafka import KafkaConsumer
import requests
import datetime
import json
import mysql.connector
from uuid import uuid4

config = {
  'user': 'root',
  'password': 'root_password',
  'host': 'mysql',
  'database': 'test_db',
  'raise_on_warnings': True
}

global connection
global cursor
connection = mysql.connector.connect(**config)
cursor = connection.cursor()

def db_entry(val):
    sql = "insert into orders(uuid, cust_id, rest_id, status, dish) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, val)
    connection.commit()

def main():
    consumer = KafkaConsumer('test', bootstrap_servers=['kafka:9092'], group_id=None, value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    print("Consumer created")

    for message in consumer:
        print("New message received")
        my_json = message.value
        print(my_json)

        uuid = str(uuid4())
        cust_id = my_json['userId']
        rest_id = my_json['restId']
        name = my_json['name']
        dish = my_json['dish']

        db_entry([(uuid, cust_id, rest_id, name, dish)])

if __name__ == '__main__':
    main()