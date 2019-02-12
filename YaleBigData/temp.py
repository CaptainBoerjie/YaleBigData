import pymysql

def todb(cursor):
	for i in range(5):
		cursor.execute("INSERT IGNORE INTO firsttable (size) VALUES (%s);",i)
		print(i)

db = pymysql.connect("localhost","root","pumpkin","Test")
cursor = db.cursor()
cursor.execute("UPDATE firsttable SET description = 'Hello You' where id = 2;")
todb(cursor)
db.commit()
