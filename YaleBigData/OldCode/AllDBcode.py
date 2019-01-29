# !/usr/bin/python3

# test to iterate through a list and insert into the db
# This code works (for some reason I have to include the bash at the beginning)
# With the 400 lines of feeds, it took 31-35 seconds to insert each feed into the database

import pymysql
import time

db = pymysql.connect("localhost","root","pumpkin","Test")
cursor = db.cursor()

path = '/home/tsotsi/Documents/Python/BigData/'
rssfile = open(path + 'newfeeds.txt','r')

feeds = rssfile.readlines()
start_time = time.time()

for line in feeds:
    lineSplit = line.split(',',3)
    sql = "INSERT IGNORE INTO feeds(fee_link, fee_source, fee_country) VALUES ('%s', '%s', '%s')" % \
    (lineSplit[3],lineSplit[1],lineSplit[2])
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print("Failed: ", lineSplit)

# disconnect from server
db.close()
print("\nRuntime: %s seconds" % (time.time() - start_time))

rssfile.close()

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

# !/usr/bin/python3
# This code populates the 'Sources' database table with the news sources for each country and corresponding number
# of feeds.

import pymysql

db = pymysql.connect("localhost","root","pumpkin","Test")
cursor = db.cursor()

query = "SELECT fee_country, fee_source, COUNT(fee_source) FROM feeds GROUP BY fee_country,fee_source;"
cursor.execute(query)
rows = cursor.fetchall()

for row in rows:
    inputquery = "INSERT IGNORE INTO sources(sou_name, sou_country, sou_feeds) VALUES ('%s', '%s', '%s')" % \
    (row[1],row[0],str(row[2]))
    print("INSERT IGNORE INTO sources(sou_name, sou_country, sou_feeds) VALUES ('%s', '%s', '%s')" % \
    (row[1],row[0],str(row[2])))
    cursor.execute(inputquery)
    db.commit()
    
db.close()

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

# !/usr/bin/python3
# this is the test with just one feed
# amazingly this works with the nytimes feed
# this now works for all text

import feedparser
from readability.readability import Document
import requests
import re
import pymysql
import time
from datetime import datetime

## cleans html tags out of text
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def convertPubdate(published):
    pythonDatetime = datetime.strptime(published[:25],'%a, %d %b %Y %H:%M:%S')
    MYsqlDatetime = pythonDatetime.strftime('%Y-%m-%d %H:%M:%S')
    return MYsqlDatetime

start_time = time.time()

db = pymysql.connect("localhost","root","pumpkin","Test")
cursor = db.cursor()

d = feedparser.parse('http://www.aljazeera.net/AljazeeraRss/Rss.aspx?URL=RSS-News.xml')

found_cnt = 0

for item in d.entries:
    found_cnt = found_cnt + 1
    response = requests.get(item["link"])
        
    doc=Document(response.content).summary()
    cleaned_docbody = cleanhtml(doc)
    SQLpublished = convertPubdate(item.published)
    
    params = ("http://www.aljazeera.net/AljazeeraRss/Rss.aspx?URL=RSS-News.xml","Al Jazeera", "Qatar", \
     SQLpublished, item.title, item.description, cleaned_docbody)
    sql_insert = """INSERT IGNORE INTO news (news_feed, news_source, news_country, news_date, \
    news_title, news_summary, news_text) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    
    
    print(sql_insert,params)
        
    cursor.execute(sql_insert,params)
    db.commit()
        
print("Added ", found_cnt," articles")

# disconnect from server
db.close()
print("\nRuntime: %s seconds" % (time.time() - start_time))

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

# The code will search for a term in the database then send the results to Repustate and take the average

# This code works, but 2018-12-2, Repustate closed connection after 910 requests.

from repustate import Client
import pymysql
import time
from datetime import datetime
from dateutil.parser import parse

start_time = datetime.now()
print("Starting at: ", start_time.strftime('%Y-%m-%d %H:%M:%S'))

search_term = '%دونالد ترامب%'

db = pymysql.connect("localhost","root","pumpkin","Test")
cursor = db.cursor()
sql_selectQuery = "SELECT news_country, news_source, news_text FROM news WHERE news_text LIKE '%دونالد ترامب%';"
cursor.execute(sql_selectQuery)
allNews = cursor.fetchall()

client = Client(api_key='853fafda33beec5ebf75ce478b47aebbc42b9f16', version='v4')
cnt = 0
sen_score = 0

for news in allNews:
    cnt = cnt + 1
    score = client.sentiment(news[2],"ar")["score"]
    sen_score = sen_score + score
    print("%s, %s, score: %s" % (news[0],news[1],str(score)))

print("\nTotal Articles: ", cnt)
print(sen_score / cnt)

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

# this code grabs a segment of text (segmentSize x 2 characters) with a search term in the middle
# then the code builds the Microsoft Azure POST json

import pymysql
import re

db = pymysql.connect("localhost","root","pumpkin","Test")
cursor = db.cursor()

searchterm = '%السعودية%'
cursor.execute("SELECT news_text FROM news WHERE news_text LIKE %s LIMIT 5;",searchterm)
allresult = cursor.fetchall()

documents = []
counter = 1

for result in allresult: 
    text = result[0]
    startindex = 0
    endindex = 0
    segmentSize = 120
    
    for m in re.finditer(searchterm[1:(len(searchterm)-1)], text):

        if m.start() < segmentSize:
            startindex = 0
        else:
            startindex = m.start() - segmentSize
        if (m.end() + segmentSize) > len(text):
            endindex = len(text)
        else:
            endindex = m.end() + segmentSize
        document = {}
        document['id'] = str(counter)
        document['language']='ar'
        document['text']=text[startindex:endindex]
        documents.append(document)
        counter=counter+1

masterdic = {}
masterdic['documents'] = documents
print(masterdic)
    
db.close()

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------

# this code grabs a segment of text (segmentSize x 2 characters) with a search term in the middle
# then the code builds the Microsoft Azure POST json

import pymysql
import re
import requests
from pprint import pprint

db = pymysql.connect("localhost","root","pumpkin","Test")
cursor = db.cursor()

searchterm = '%السعودية%'
cursor.execute("SELECT news_text FROM news WHERE news_text LIKE %s LIMIT 5;",searchterm)
allresult = cursor.fetchall()

documents = []
counter = 1

for result in allresult: 
    text = result[0]
    text = text[1000:]
    startindex = 0
    endindex = 0
    segmentSize = 120
    
    for m in re.finditer(searchterm[1:(len(searchterm)-1)], text):

        if m.start() < segmentSize:
            startindex = 0
        else:
            startindex = m.start() - segmentSize
        if (m.end() + segmentSize) > len(text):
            endindex = len(text)
        else:
            endindex = m.end() + segmentSize
        document = {}
        document['id'] = str(counter)
        document['language']='ar'
        document['text']=text[startindex:endindex]
        documents.append(document)
        counter=counter+1

masterdic = {}
masterdic['documents'] = documents
print(masterdic)
    
db.close()

# -----------------------------------------------------------

subscription_key = 'b8695a160e534e488f8c17082124397b'
assert subscription_key

text_analytics_base_url = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/"

sentiment_api_url = text_analytics_base_url + "sentiment"

headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
response  = requests.post(sentiment_api_url, headers=headers, json=masterdic)
sentiments = response.json()
pprint(sentiments)

---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------



---------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------