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

def create_restaurent(val):
    sql = "INSERT INTO restaurent(rid, name) VALUES (%s, %s)"
    cursor.executemany(sql, val)
    connection.commit()

def update_status(val):
    sql = "update orders set status = %s where uuid = %s"
    cursor.executemany(sql, val)
    connection.commit()

app = Flask(__name__)

# To create new restaurant entries in the database
@app.route('/restaurant/create', methods=["Post"])
def create():
    content = request.data
    post_json = json.loads(content)

    rest_id = post_json['restId']
    name = post_json['name']

    create_restaurent([(rest_id, name)])

    my_response = post_json
    return make_response(jsonify(my_response), 200)

# To change the status of a customer's order
@app.route('/restaurant/update', methods=["Put"])
def update():
    orderId = request.args.get('orderId')
    status =  request.args.get('status')


    status = update_status([(status, orderId)])

    post_json = {'orderId': orderId, 'status': status, 'response': 'success'}
    my_response = post_json
    return make_response(jsonify(my_response), 200)

if __name__ == '__main__':
    app.run(debug=True, port=7007, host='0.0.0.0')