# Simple script to remove trailing '\n' from the RSS feed hyperlinks in the database

import pymysql

db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
cursor = db.cursor()

cursor.execute("SELECT fee_id, fee_link FROM feeds ORDER BY fee_id;")
feeds = cursor.fetchall()

totalchanges = 0
for feed in feeds:
    if "\n" in feed[1]:
        cursor.execute("UPDATE feeds SET fee_link = %s WHERE fee_id = %s;",(feed[1].rstrip(),feed[0]))
        db.commit()
        totalchanges += 1
    else:
        pass

print("Total changes: ", totalchanges)
db.close()
