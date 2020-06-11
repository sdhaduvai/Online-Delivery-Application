from flask import Flask, jsonify, request, abort, make_response
from kafka import KafkaProducer
import requests
import datetime
import json
from uuid import uuid4
import mysql.connector

producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

config = {
  'user': 'root',
  'password': 'root_password',
  'host': 'mysql',
  'database': 'test_db',
  'raise_on_warnings': True
}

connection = mysql.connector.connect(**config)

cursor = connection.cursor()

def existing_customer(val):
    sql = "select * from customer where userId = %s"
    cursor.execute(sql, (val, ))

    if len(cursor.fetchall()) == 0:
        return False

    return True

def new_user_entry(val):
    sql = "INSERT INTO customer(userId, name) VALUES (%s, %s)"
    cursor.executemany(sql, val)
    connection.commit()

def check_order_status(val):
    sql = "select * from orders where uuid = %s"
    cursor.execute(sql, (val, ))
    result = cursor.fetchall()
    print(result)
    return result[0][3]

app = Flask(__name__)
# To create a new order for a customer
@app.route('/order', methods = ["Post"])
def create():
    content = request.data
    post_json = json.loads(content)

    cust_id = post_json['userId']
    restId = post_json['restaurant_id']
    name = post_json['name']
    dish = post_json['cust_order']

    if existing_customer(cust_id):
        pass
    else:
        new_user_entry([(cust_id, name)])

    producer.send('test', value = post_json)

    my_response = post_json
    return make_response(jsonify(my_response), 200)

# To get the status of an order placed by a customer
@app.route('/order/status/<orderId>', methods=["Get"])
def status(orderId):
    status = check_order_status(orderId)
    print(status)
    post_json = {'orderId': orderId, 'status': status}
    my_response = post_json
    return make_response(jsonify(my_response), 200)

if __name__ == '__main__':
    app.run(debug=True, port=7006, host='0.0.0.0')