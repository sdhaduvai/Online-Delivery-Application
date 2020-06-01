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

sql = "select * from orders where uuid = %s"
val = '12dcfd85-22bd-4346-a3b0-ecfe2bf8995b'

cursor.execute(sql, (val,))
result = cursor.fetchall()
print(result[0][3])