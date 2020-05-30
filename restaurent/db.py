import mysql.connector

config = {
  'user': 'root',
  'password': 'root_password',
  'host': '127.0.0.1',
  'database': 'test_db',
  'raise_on_warnings': True
}

connection = mysql.connector.connect(**config)

cursor = connection.cursor()

sql = "INSERT INTO orders ( userId, name, dish ) VALUES ( %s, %s, %s )"
val = [(5, "Sreekar", "Idli")]

cursor = connection.cursor()
cursor.executemany(sql, val)
connection.commit()