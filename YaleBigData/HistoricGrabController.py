# This code will control the historic and archived article scrapes.  It will 
# handle timeout exceptions and maintain the position of the last scraped
# article.
# As an example, Algeria's El Heddaf newspaper formats the article URLs as such:
# http://www.elheddaf.com/article/detail?id=0000000
# The id number '00000000' is a unique identifier for the article.
# For websites with similar formats, it is simple to iterate through the articles
# and scrape.

# CSV file for sources capable of iterative scraping named HistoricGrabList.csv

import csv
import pymysql
import datetimehandler
import os
from datetime import datetime
from requests import exceptions as reqEx
from selenium.common import exceptions as selEx

grablist = []
with open('HistoricGrabList.csv','r') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        grablist.append(row)


db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
cursor = db.cursor()

start_time = datetime.now()

print(grablist)
for entry in grablist: # country, source, url, min, max
    currentID = int(entry[3])
    maxID = int(entry[4])
    activelinks = 0
    deadlinks = 0
    links404 = 0
    selerror = 0

    codelocation = "SeleniumBeautifulSoup." + entry[0] + "." +entry[1] + '_grabSingleArticle'
    sourceImport = __import__(codelocation, fromlist = [None])
    
    while currentID < maxID:
        tgt_url = str(currentID).join(entry[2].split('*'))

        try:
            receivedScrape = sourceImport.grabPage(tgt_url) # title, date article
            if receivedScrape[0] is not None:
                date = datetimehandler.convertRSSdate(receivedScrape[1])
                params = (tgt_url,entry[1], entry[0], date, receivedScrape[0], receivedScrape[2], tgt_url)
                sql_insert = """INSERT IGNORE INTO news (news_feed, news_source, news_country, news_date, \
                   news_title, news_text, news_link) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql_insert,params)
                db.commit()
                activelinks += 1
            else:
                links404 += 1

        except reqEx.RequestException:
            deadlinks += 1
            # write i to csv file and 'grablist' to update position
        except selEx.TimeoutException:
            # Timeout in Selenium, not a broken link, so retry currentID
            deadlinks += 1
        except selEx.WebDriverException as e:
            # connection refused, try again
            currentID -= 1
            selerror += 1
        finally:
            entry[3] = str(currentID)
            os.system('clear')
            print("Current scrape")
            print("{}: {}: {} of {}".format(entry[0],entry[1],currentID,maxID))
            print("----\n {} active links\n {} dead links\n {} 404 links\n {} Selenium exceptions".format(activelinks,deadlinks,links404,selerror))
            print("\nRuntime: %s seconds" % (str(datetime.now() - start_time)))
            currentID += 1

db.close()

"""
Add the following code to all _grabSingleArticle.py file to catch NoneType
Exceptions and remove need to test against every 404 page:

title = soup.find('div',attrs={'class':'helloeverybody'})
try:
    print(title.text.strip())
except AttributeError as e:
    return([None,None,None])

"""
