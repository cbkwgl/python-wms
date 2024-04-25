import sqlite3

connection = sqlite3.connect("wms.db", check_same_thread=False)
cursor = connection.cursor()
cursor.execute("SELECT * FROM GOODS_RECEIPT")

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.execute("SELECT * FROM AUDIT")
rows = cursor.fetchall()

for row in rows:
    print(row)
