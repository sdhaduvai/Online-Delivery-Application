from flask import Flask, jsonify, request, abort, make_response
from kafka import KafkaConsumer
import requests
import datetime
import json
import mysql.connector

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
    sql = "INSERT INTO orders ( userId, name, dish ) VALUES ( %s, %s, %s )"
    cursor.executemany(sql, val)
    connection.commit()

def main():
    print("REACHED HERE")
    consumer = KafkaConsumer('test', bootstrap_servers=['kafka:9092'], group_id=None, value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    print("Consumer created")

    for message in consumer:
        print("New message received")
        my_json = message.value
        print(my_json)

        userId = my_json['id']
        name = my_json['name']
        dish = my_json['dish']
        val = [(userId, name, dish)]
        db_entry(val)

if __name__ == '__main__':
    main()