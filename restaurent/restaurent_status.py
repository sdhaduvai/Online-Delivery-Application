from flask import Flask, jsonify, request, abort, make_response
from kafka import KafkaProducer
import requests
import datetime
import json
from uuid import uuid4

config = {
    'user': 'root',
    'password': 'root_password',
    'host': '127.0.0.1',
    'database': 'test_db',
    'raise_on_warnings': True
}

connection = mysql.connector.connect(**config)

cursor = connection.cursor()

def create_restaurent(val):
    sql = "INSERT INTO restaurent(rid, name) VALUES (%s, %s)"
    cursor.executemany(sql, val)
    connection.commit()

def update_status(val):
    sql = "update table orders set status = %s where uuid = %s"
    cursor.executemany(sql, val)
    connection.commit()

app = Flask(__name__)

# To consume latest messages and auto-commit offsets
@app.route('/create_restaurent', methods=["Post"])
def main():
    content = request.data
    post_json = json.loads(content)

    rest_id = post_json['restId']
    name = post_json['name']

    create_restaurent([(rest_id, name)])

    my_response = post_json
    return make_response(jsonify(my_response), 200)

# To consume latest messages and auto-commit offsets
@app.route('/update_status', methods=["Post"])
def main():
    content = request.data
    post_json = json.loads(content)

    uuid = post_json['orderId']
    new_status = post_json['status']

    status = update_status([uuid, new_status])

    post_json = {'orderId': uuid, 'status': status, 'response': 'success'}
    my_response = post_json
    return make_response(jsonify(my_response), 200)

if __name__ == '__main__':
    app.run(debug=True, port=7006, host='0.0.0.0')