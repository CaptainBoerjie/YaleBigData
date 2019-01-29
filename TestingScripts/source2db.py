import pymysql

db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
cursor = db.cursor()

with open('SourceList.txt','r') as f:
    for x in f:
        print(x)
        country = x.rsplit(",")[0]
        link = x.rstrip('\n').split(',')[1]
        sou_id = input("Enter id #: ")
        cursor.execute("UPDATE sources SET sou_link = %s WHERE sou_id = %s;",(link,sou_id))
        db.commit()

db.close