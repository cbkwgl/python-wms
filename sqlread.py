import sqlite3

connection = sqlite3.connect("wms.db", check_same_thread=False)
cursor = connection.cursor()
print("GOODS RECEIPT")
cursor.execute("SELECT * FROM GOODS_RECEIPT")

rows = cursor.fetchall()

for row in rows:
    print(row)

print("AUDIT")
cursor.execute("SELECT * FROM AUDIT")
rows = cursor.fetchall()

for row in rows:
    print(row)

print("PRODUCT QTY")
cursor.execute("SELECT * FROM PRODUCT_QTY")
rows = cursor.fetchall()

for row in rows:
    print(row)

print("SHIPMENT")
cursor.execute("SELECT * FROM SHIPMENT_INBOUND")
rows = cursor.fetchall()

for row in rows:
    print(row)
