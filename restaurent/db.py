import mysql.connector
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

sql = "select * from customer where userId = %s"
val = 5

cursor.execute(sql, (val,))
result = cursor

print(result.fetchall()[0][0])