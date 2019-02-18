# Grab the daily statistics of the database and write to a csv file.
# Total articles, articles by country, articles by source (include updated)
"""
CSV Format:
Date, Total Articles, #
Updated Date, Country, #
Updated Date, Country, Source, #
.
.
.
"""


import pymysql
import csv
from datetime import datetime

db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
cursor = db.cursor()

with open('PeriodicStatistics.csv', mode='ab') as file:
    writer = csv.writer(file, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    cursor.execute("SELECT count(*) FROM news;")
    count = cursor.fetchone()[0]

    writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'Total Articles',count])

    cursor.execute("SELECT * FROM countries;")
    countries = cursor.fetchall()
    for country in countries:
        cursor.execute("SELECT count(*) FROM news WHERE news_country=%s;",(country[0]))
        count = cursor.fetchone()
        writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),country[0],count[0]])

        cursor.execute("SELECT * FROM sources WHERE sou_country = %s;",(country[0]))
        sources = cursor.fetchall()
        for source in sources:
            cursor.execute("SELECT count(*) FROM news WHERE news_country = %s AND news_source = %s;",(country[0],source[1]))
            count = cursor.fetchone()
            writer.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'),source[3],country[0],source[1],count[0]])

db.close()
