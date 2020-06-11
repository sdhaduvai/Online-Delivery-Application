from flask import Flask, jsonify, request, abort, make_response
from kafka import KafkaProducer
import requests
import datetime
import json
from uuid import uuid4
import mysql.connector

config = {
    'user': 'root',
    'password': 'root_password',
    'host': 'mysql',
    'database': 'test_db',
    'raise_on_warnings': True
}

connection = mysql.connector.connect(**config)

cursor = connection.cursor()

def create_restaurant(val):
    sql = "INSERT INTO restaurant(restId, name) VALUES (%s, %s)"
    cursor.executemany(sql, val)
    connection.commit()

def update_status(val):
    sql = "update orders set status = %s where uuid = %s"
    cursor.executemany(sql, val)
    connection.commit()

app = Flask(__name__)

# To create new restaurant entries in the database
@app.route('/restaurant', methods=["Post"])
def create():
    content = request.data
    post_json = json.loads(content)

    rest_id = post_json['restaurant_id']
    name = post_json['name']

    create_restaurant([(rest_id, name)])

    my_response = post_json
    return make_response(jsonify(my_response), 200)

# To change the status of a customer's order
@app.route('/restaurant/update', methods=["Put"])
def update():
    content = request.data
    post_json = json.loads(content)

    orderId = post_json['orderId']
    status = post_json['status']

    update_status([(status, orderId)])

    post_json = {'orderId': orderId, 'status': status, 'response': 'success'}
    my_response = post_json
    return make_response(jsonify(my_response), 200)

if __name__ == '__main__':
    app.run(debug=True, port=7007, host='0.0.0.0')