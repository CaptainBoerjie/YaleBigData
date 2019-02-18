# Simple script to remove spaces from source names in DB.  Spaces will throw an error 
# when controller code attempts to dynamically import source related code based on 
# source name.

import pymysql

db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
cursor = db.cursor()

cursor.execute("SELECT news_id,news_source FROM news;")

sources = cursor.fetchall()
for source in sources:
    cursor.execute("UPDATE news SET news_source = %s WHERE news_id = %s;",(''.join(source[1].split()), source[0]))
    db.commit()

db.close()
