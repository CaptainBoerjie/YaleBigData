import feedparser
from newspaper import Article
import pymysql
import datetimehandler
from datetime import datetime
from requests import exceptions as reqEx
import os


# -----------------------------------------------------------------------------
# ---------------------------------RSS FEED HANDLER----------------------------
# -----------------------------------------------------------------------------

def handle_rss(source, country, cursor, feed_type):
    cursor.execute("SELECT * FROM feeds WHERE fee_country=%s AND fee_source=%s;", (country,source))
    feeds = cursor.fetchall()
    for f in feeds:
        feed = feedparser.parse(f[1])
        print("Feed: {} with {} articles".format(f[1],len(feed.entries)))
        totalerrors = 0
        for item in feed.entries:
            
            try: 
                raw_published = item.published
                print("Success - Pulled date from RSS")

            except: 
                raw_published = ''
                totalerrors += 1

            article_title = item.title
            article_link = item.link
            article_text = ''

            try: # Try to access the main article linked in the RSS xml data

                if feed_type == 'Newspaper':
                    article = Article(item.link)
                    article.download()
                    article.parse()
                    # toi_article.title and toi_article.text
                    article_text = article.text
                    try: article_title = article.title
                    except: totalerrors += 1
                    print("Success - Pulled Newspaper")
            
                elif feed_type == 'BeautifulSoup':

                    codelocation = "SeleniumBeautifulSoup." + entry[0] + "." +entry[1] + '_grabSingleArticle'
                    sourceImport = __import__(codelocation, fromlist = [None])
                    try:
                        receivedScrape = sourceImport.grabPage(article_link) # title, date article
                        if receivedScrape[0] is not None:
                            article_text = receivedScrape[2]
                        else:
                            totalerrors += 1

                    except reqEx.RequestException:
                        article_text = None
                        totalerrors += 1

            except: # Main article link either broken or not present in feed
                article_text = None
                totalerrors += 1

            if article_link == None or article_text == None or article_title == None:
                totalerrors += 1
            else:
                publishedDate = datetimehandler.convertRSSdate(raw_published)
                updated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print("Published: ", publishedDate)
                print("Current Time: ", updated_time)
                print("Last update: ", f[4])

                if f[4] < publishedDate:
                    print("Writing article to DB")
                    cursor.execute("UPDATE feeds SET fee_updated = %s WHERE fee_id = %s;",(updated_time,f[0]))
                    params = (f[0],source, country, publishedDate, article_title, article_text, article_link)
                    sql_insert = """INSERT IGNORE INTO news (news_feed, news_source, news_country, news_date, \
                    news_title, news_text, news_link) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql_insert,params)
                    print("Executed article push to DB")

                else: 
                    print("Article older than last update (won't push to DB)")

        print("Total errors in feed: {}\n".format(totalerrors))

# -----------------------------------------------------------------------------
# ---------------------------------SELENIUM - BS - HANDLER --------------------
# -----------------------------------------------------------------------------    

def handle_SelBS(source, country, cursor):
    pass

# -----------------------------------------------------------------------------
# ---------------------------------MAIN CODE-----------------------------------
# -----------------------------------------------------------------------------

start_time = datetime.now()

db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
cursor = db.cursor()

cursor.execute("SELECT * FROM sources WHERE sou_type LIKE %s AND sou_country = 'Tunisia' LIMIT 2;",("%RSS%"))
sources = cursor.fetchall()

for source in sources: # id, source, country, updated, feeds, type, logo, link
    try:
        #os.system('clear')
        print("{} : {}".format(source[2],source[1]))
        print("Feeds: {} | Type: {}".format(source[4],source[5]))

        if source[5][0:3] == 'RSS':
            handle_rss(source[1],source[2],cursor,source[5][4:])
            db.commit()
            
        elif source[5] == 'Selenium-BeautifulSoup':
            handle_SelBS(source[2],source[1],cursor)

    except:
        pass

    finally:
        today = datetime.now()
        updated_time = today.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE sources SET sou_updated = %s WHERE sou_id = %s;",(updated_time,source[0]))
        db.commit()
        print("Committed updates to DB")
        print("---Total running time: ", (str(datetime.now() - start_time)))


db.close()
print("\nFinal Runtime: %s seconds" % (str(datetime.now() - start_time)))
