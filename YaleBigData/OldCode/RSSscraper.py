# News scraper in the following steps
# 1 - Get feed from DB
# 2 - Pull feed (feedparser)
# 3 - Grab link from feed
# 4 - Pull individual article (newspaper)
# 5 - Push news item to DB

import feedparser
import newspaper
from readability.readability import Document
import requests
import re
import pymysql
import time
from datetime import datetime
from dateutil.parser import parse

# -------------- 
def iterateFeed():
    # IN: 
    # OUT:
    # 
    code
    
# --
def scrapeFeed(rssURL):
    # IN: feed url from 'feeds' database
    # OUT: Parsed RSS _________
    
    feed_time = datetime.now()
    feed = feedparser.parse(rssURL)

    # Iterate through each news item in the RSS feed
    for item in feed.entries:

        try: # Try to convert RSS publication datetime format to MySQL datetime format
            SQLpublished = convertPubdate(item.published,row[3], row[2], row[0])        
        except: # If converstion function fails, code will insert 'NULL' into 'news_date' field
            SQLpublished = None
    
#----
def pullArticle():
    # IN: article link from RSS feed, date from RSS feed
    # OUT: List [ Pubdate, Title, Text ]
    # 
    news = newspaper.build('http://www.akhbarelyaom.com/')

    for article in news.articles:
        print(article.url)
        article.download()
        article.parse()
        print(article.title)
    
# ----
def insertArticle():
    code
    
# ---------------------------------------------- LOG FUNCTIONS -----------------------------------------

def errlog(error,country,source,feed):
    errors = [
        "No usable publication date",
        "Broken article link from feed",
        "Unable to insert feed information",
        "Error while updating feed datetime",
        "Server rejected connection",
        "Unable to parse feed"
    ]
    
    path = '/home/tsotsi/Documents/Python/BigData/'
    errlogfile = open(path + 'log_error.txt','a')
    
    today = datetime.now()
    errorDatetime = today.strftime('%Y-%m-%d %H:%M:%S')
    
    compilederror = errorDatetime + "," + errors[error] + "," + country + "," + source + "," + str(feed) + "\n"
    errlogfile.write(compilederror)
    errlogfile.close()

# ----------------------------------------------   

def activitylog(activity, *args, **kwargs):
    activities = {
        "1":"RSS main scrape started",
        "2":"Total scrape time",
        "3":"Total new articles",
        "4":"RSS main scrape ended",
        "5":"Scrape time for country",
        "6":"Scrape time for source",
        "7":"Scrape time for feed",
        "8":"New articles added for country",
        "9":"New articles added for source",
        "10":"New articles added for feed",
        "11":"RSS entries passed over"
    }
    
    path = '/home/tsotsi/Documents/Python/BigData/'
    logfile = open(path + 'log_activity.txt','a')
    
    today = datetime.now()
    actDatetime = today.strftime('%Y-%m-%d %H:%M:%S')    
    
    if activity is "1": # RSS main scrape started
        towrite = actDatetime +","+ activities["1"] +","+ args[0].strftime('%Y-%m-%d %H:%M:%S') + "\n"
        logfile.write(towrite)
    elif activity is "2": # Total scrape time
        endtime = datetime.now() - args[0]
        towrite = actDatetime +","+ activities["2"] +","+ str(endtime) + "\n"
        logfile.write(towrite)
    elif activity is "3": # Total new articles
        towrite = actDatetime +","+ activities["3"] +","+ str(args[0]) + "\n"
        logfile.write(towrite)
    elif activity is "7": # Total time for feed
        endtime = datetime.now() - args[0]
        towrite = actDatetime +","+ activities["7"] +","+ kwargs['country'] +","+ kwargs['source'] +","+ str(kwargs['feed']) +","+ str(endtime) +"\n"
        logfile.write(towrite)
    elif activity is "10": # Total articles for feed
        towrite = actDatetime +","+ activities["10"] +","+ kwargs['country'] +","+ kwargs['source'] +","+ str(kwargs['feed']) +","+ str(args[0]) +"\n"
        logfile.write(towrite)
    elif activity is "11": # RSS feeds passed over
        towrite = actDatetime +","+ activities["10"] +","+ str(args[0])
        logfile.write(towrite)
        
    logfile.close()
        

# ----------------------------------------------   MAIN CODE   -----------------------------------------
    
start_time = datetime.now()
print("Starting at: ", start_time.strftime('%Y-%m-%d %H:%M:%S'))
activitylog("1",start_time)

db = pymysql.connect("localhost","root","pumpkin","Test")
cursor = db.cursor()
sql_selectQuery = "SELECT * FROM feeds;"
cursor.execute(sql_selectQuery)
allFeeds = cursor.fetchall()

found_cnt = 0
passed_entries = 0

for row in allFeeds:    # for-loop to iterate through entire list of RSS feeds
    # row[0] - fee_id
    # row[1] - fee_link
    # row[2] - fee_source
    # row[3] - fee_country
    # row[4] - fee_updated

    out = scrapeFeed(row[1])

