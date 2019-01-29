# !/usr/bin/python3
# Code works but still has trouble identifying if article new or not, many feeds don't use easy to convert datetimes
# converts most pubDate formats using dateutils but those with +0300 type timezone info are converted to current datetime


import feedparser
from readability import Document
import requests
import re
import pymysql
import time
from datetime import datetime
from dateutil.parser import parse


# ----------------------------------------------------------------------------------------------------------------------    
## cleans html tags and random numbers and symbols out of text
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    stopterms = ['&#13;','13#&','&#13','\n','\xa0']
    querywords = cleantext.split()
    resultwords  = [word for word in querywords if word.lower() not in stopterms]
    clean = ' '.join(resultwords)

    pattern = r"[(&#\-,،;:\'\")]".format(remove) # create the pattern
    pattern2 = r"[0-9]".format(remove) # create the pattern
    clean =re.sub(pattern, "", news[1], re.UNICODE)
    clean =re.sub(pattern2,"", clean, re.UNICODE)
    try:
        front_space = lambda x:x[0]==" "
        trailing_space = lambda x:x[-1]==" "
        clean = " "*front_space(clean)+' '.join(clean.split())+" "*trailing_space(clean)
    except:
        pass
    return clean

# ----------------------------------------------------------------------------------------------------------------------    

def convertPubdate(published,*args):
    try: 
        cleanDate = parse(published, fuzzy_with_tokens=True, ignoretz=True)
        strCleanDate = cleanDate[0].strftime('%Y-%m-%d %H:%M:%S')
        return strCleanDate
    except:
        if(published[-5] is '+'):
            try:
                cleanDate = parse(published[:25], fuzzy_with_tokens=True, ignoretz=True)
                strCleanDate = cleanDate[0].strftime('%Y-%m-%d %H:%M:%S')
            except:
                today = datetime.now()
                strCleanDate = today.strftime('%Y-%m-%d %H:%M:%S')
                errlog(0,args[0],args[1],args[2])
                print("No usable date, using current date.")
        else:
            today = datetime.now()
            strCleanDate = today.strftime('%Y-%m-%d %H:%M:%S')
            errlog(0,args[0],args[1],args[2])
            print("No usable date, using current date.")
        return strCleanDate
    
# ----------------------------------------------------------------------------------------------------------------------    
    
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

# ----------------------------------------------------------------------------------------------------------------------    

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
        
# ----------------------------------------------------------------------------------------------------------------------    

def checkarticle(country,source,title,published,feedtime,lastupdate):
    strfeedtime = feedtime.strftime('%Y-%m-%d %H:%M:%S')

    if lastupdate is None:
        return 0
    if published is None: # Published date from RSS is NULL (not present), check if already in database
        query = "SELECT news_id FROM news WHERE news_country = %s AND news_source = %s AND news_title = %s"
        parameters = (country,source,title)
        cursor.execute(query,parameters)
        rows = cursor.rowcount
        return rows # if present in database, rows will be greater than 0 and article won't be inserted
    if published > strfeedtime: 
        return 0 # published datetime after start of feed processing: pubDate was incompatible so time of check was used
    elif published < lastupdate.strftime('%Y-%m-%d %H:%M:%S'):
        return 1 # article date older than last update so was already inserted on previous run
    else:
        return 0 # last resort, insert article and any duplicates will be removed on cleanup

# ----------------------------------------------------------------------------------------------------------------------    

# ---------------- Start of main code ----------------
# row[0] - id, row[1] - feed url, row[2] - source, row[3] - country

start_time = datetime.now()
print("Starting at: ", start_time.strftime('%Y-%m-%d %H:%M:%S'))
activitylog("1",start_time)

db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
cursor = db.cursor()
sql_selectQuery = "SELECT * FROM feeds;"
cursor.execute(sql_selectQuery)
allFeeds = cursor.fetchall()

found_cnt = 0
passed_entries = 0

# Read first RSS feed from feeds list
for row in allFeeds:
    feedArticles = 0

#    try: # Try to parse the xml information from the RSS feed link
    feed_time = datetime.now()
    feed = feedparser.parse(row[1])

    # Iterate through each news item in the RSS feed
    for item in feed.entries:

        try: # Try to convert RSS publication datetime format to MySQL datetime format
            SQLpublished = convertPubdate(item.published,row[3], row[2], row[0])        
        except: # If converstion function fails, code will insert 'NULL' into 'news_date' field
            SQLpublished = None

        # Based on the article published date, determine if it is new or old
        if checkarticle(row[3],row[2],item.title, SQLpublished, feed_time, row[4]) is 0:              
            feedArticles = feedArticles + 1
            found_cnt = found_cnt + 1
            try: # Try to access the main article linked in the RSS xml data
                response = requests.get(item.link)

                # Clean the main article text
                doc=Document(response.content).summary()
                cleaned_docbody = cleanhtml(doc)
                # If the news server rejects the request, 
                # it may return 'Access Denied' instead of killing the connection
                if 'Access Denied' in cleaned_docbody:
                    cleaned_docbody = None
                doclink = item.link
            except: # Main article link either broken or not present in feed
                errlog(1,row[3], row[2], row[0])
                doclink = None
                cleaned_docbody = None

            try: # Check to see if the RSS feed has a summary or description field
                description = item.description
            except: # Otherwise insert 'NULL' into 'news_summary' field
                description = None

            # Build the MySQL insert code
            params = (row[1],row[2], row[3], SQLpublished, item.title, description, cleaned_docbody, doclink)
            sql_insert = """INSERT IGNORE INTO news (news_feed, news_source, news_country, news_date, \
            news_title, news_summary, news_text, news_link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""   
            try: # Attempt to insert the MySQL statement
                cursor.execute(sql_insert,params)
                db.commit()
            except: # If MySQL insert fails, rollback request and update error log
                passed_entries = passed_entries + 1
                db.rollback()
                print("Error in country: %s, Source: %s, Feed: %s" % (row[3],row[2],row[1]))
    try: # Finally, update the time the feed was updated
        rightnow = datetime.now()
        strUpdateDate = rightnow.strftime('%Y-%m-%d %H:%M:%S')        
        cursor.execute("UPDATE feeds SET fee_updated=%s WHERE fee_id=%s;", (strUpdateDate,row[0]))
        db.commit()
    except: # There should not be an error, but exception handles any possible issues with feed changes
        db.rollback()
        print("Error while updating feed date: %s, %s, %s" % (row[3], row[2], row[1]))
    # Update activity log with feed time and new feed articles
    activitylog("7",feed_time,country=row[3], source=row[2], feed=row[0])
    activitylog("10",feedArticles,country=row[3], source=row[2], feed=row[0])

#    except:
#        print("Error connecting or parsing data from: %s, %s, %s" % (row[3], row[2], row[1]))
#        errlog(5,row[3], row[2], row[1])
    
# disconnect from server
db.close()

print("\nAdded ", found_cnt," articles")
print("RSS entries passed over: ", passed_entries)
print("\nRuntime: %s seconds" % (str(datetime.now() - start_time)))

activitylog("2",start_time)
activitylog("3",found_cnt)
activitylog("11",passed_entries)