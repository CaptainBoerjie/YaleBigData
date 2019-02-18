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
    sourceArticles = 0
    for f in feeds:
        feed = feedparser.parse(f[1])
        print("Feed: {} with {} articles".format(f[1],len(feed.entries)))
        totalerrors = 0
        for item in feed.entries:
            
            try:
                try:
                    raw_published = item.published
                except:
                    raw_published = item.updated
                publishedDate = datetimehandler.convertRSSdate(raw_published)
                updated_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                lastupdate = f[4]
                lastupdate = lastupdate.strftime('%Y-%m-%d %H:%M:%S')

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
            
                elif feed_type == 'BeautifulSoup':

                    codelocation = "SeleniumBeautifulSoup." + entry[0] + "." +entry[1] + '_grabSingleArticle'
                    sourceImport = __import__(codelocation, fromlist = [None])
                    try:
                        receivedScrape = sourceImport.grabPage(article_link) # title, date article
                        if receivedScrape[0] is not None:
                            article_text = receivedScrape[2]
                            if publishedDate == '':
                                try:
                                    publishedDate = datetimehandler.convertRSSdate(receivedScrape[1])
                                except:
                                    print("--ERROR no RSS date and no BS date--")
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
            elif lastupdate < publishedDate:
                cursor.execute("UPDATE feeds SET fee_updated = %s WHERE fee_id = %s;",(updated_time,f[0]))
                params = (f[1],source, country, publishedDate, article_title, article_text, article_link)
                sql_insert = """INSERT IGNORE INTO news (news_feed, news_source, news_country, news_date, \
                news_title, news_text, news_link) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql_insert,params)
                sourceArticles += 1
            else: 
                pass

    print("Total errors in source ({}): {}".format(source,totalerrors))
    print("Total articles added for {} | {}: {}".format(country,source,sourceArticles))

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

cursor.execute("SELECT * FROM sources;")
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
        print("---Total running time: {}\n".format(str(datetime.now() - start_time)))


db.close()
print("\nFinal Runtime: %s seconds" % (str(datetime.now() - start_time)))
