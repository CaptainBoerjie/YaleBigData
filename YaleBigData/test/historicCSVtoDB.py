import csv
import pymysql

db = pymysql.connect('localhost','root','pumpkin','ScrapeDB')
cursor = db.cursor()

grablist = []
with open('../HistoricGrabList.csv','r') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        grablist.append(row)

for row in grablist:
    params = (row[0],row[1],row[2],row[3],row[4])
    sqlinsert = "INSERT IGNORE INTO historic (his_country,his_source,his_url,his_min,his_max) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sqlinsert,params)
    db.commit()

db.close()

