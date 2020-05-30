from flask import Flask, jsonify, request, abort, make_response
from kafka import KafkaProducer
import requests
import datetime
import json
from uuid import uuid4

producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

config = {
  'user': 'root',
  'password': 'root_password',
  'host': '127.0.0.1',
  'database': 'test_db',
  'raise_on_warnings': True
}

connection = mysql.connector.connect(**config)

cursor = connection.cursor()

def existing_customer(val):
    sql = "select * from customer where userId = %s"
    cursor.execute(sql, (val, ))
    count = cursor.rowcount
    if count == 0:
        return False
    return True

def add_order_to_db(val):
    sql = "insert into orders(uuid, cust_id, rest_id, status, dish) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql, val)
    connection.commit()

def new_user_entry(val):
    sql = "INSERT INTO customer(userId, name) VALUES (%s, %s)"
    cursor.executemany(sql, val)
    connection.commit()

def check_order_status(val):
    sql = "select * from orders where uuid = %s"
    cursor.execute(sql, (val, ))
    cursor.fetchall()

app = Flask(__name__)
# To consume latest messages and auto-commit offsets
@app.route('/create_order', methods = ["Post"])
def main():
    content = request.data
    post_json = json.loads(content)

    cust_id = post_json['userId']
    rest_id = post_json['restId']
    name = post_json['name']
    dish = post_json['dish']

    if existing_customer(cust_id):
        uuid = str(uuid4())
        add_order_to_db([(uuid, cust_id, rest_id, "CREATED", dish)])
    else:
        new_user_entry([(cust_id, "name")])
        uuid = str(uuid4())
        add_order_to_db([(uuid, cust_id, rest_id, "CREATED", dish)])

    producer.send('test', value = post_json)

    my_response = post_json
    return make_response(jsonify(my_response), 200)

# To consume latest messages and auto-commit offsets
@app.route('/check_status', methods=["Post"])
def main():
    content = request.data
    post_json = json.loads(content)

    uuid = post_json['orderId']

    status = check_order_status(uuid)

    post_json = {'orderId': uuid, 'status': status}
    my_response = post_json
    return make_response(jsonify(my_response), 200)

if __name__ == '__main__':
    app.run(debug=True, port=7006, host='0.0.0.0')