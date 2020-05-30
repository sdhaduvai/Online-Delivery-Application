from flask import Flask, jsonify, request, abort, make_response
from kafka import KafkaProducer
import requests
import datetime
import json

producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def existing_customer(val):
    sql = "select * from customer where userId = %s"
    cursor.executemany(sql, val)

def db_entry(val):
    sql = "INSERT INTO customer(userId, name, dish) VALUES ( %s, %s, %s )"
    cursor.executemany(sql, val)
    connection.commit()

app = Flask(__name__)
# To consume latest messages and auto-commit offsets
@app.route('/create_order', methods = ["Post"])
def main():
    content = request.data
    post_json = json.loads(content)

    id = post_json['userId']
    name = post_json['name']
    order = post_json['order']

    val = [(id, name, order)]

    if existing_customer(val):


    producer.send('test', value = post_json)

    my_response = post_json
    return make_response(jsonify(my_response), 200)

if __name__ == '__main__':
    app.run(debug=True, port=7006, host='0.0.0.0')