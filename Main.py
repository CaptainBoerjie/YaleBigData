import feedparser
from newspaper import Article
from readability.readability import Document
import requests
import re
import pymysql
import datetimehandler
from datetime import datetime


# -----------------------------------------------------------------------------
# ---------------------------------RSS FEED HANDLER----------------------------
# -----------------------------------------------------------------------------

def handle_rss(source, country, cursor, feed_type):
    cursor.execute("SELECT * FROM feeds WHERE fee_country=%s AND fee_source=%s;", (country,source))
    feeds = cursor.fetchall()
    for f in feeds:
        feed = feedparser.parse(f[1])
        for item in feed.entries:

            try: raw_published = item.published
            except: raw_published = ''

            article_title = item.title
            article_link = item.link

            try: # Try to access the main article linked in the RSS xml data

                if feed_type == 'Newspaper':
                    article = Article(item.link)
                    article.download()
                    article.parse()
                    # toi_article.title and toi_article.text
                    article_text = article.text
                    try: article_title = article.title
                    except: pass
                    try: raw_published = article.published_date
                    except: raw_published = ''
            
                elif feed_type == 'Readability':
                    response = requests.get('https://www.lebanon24.com/Rss/News/1/%D9%84%D8%A8%D9%86%D8%A7%D9%86')
                    raw_html=Document(response.text).summary()

                    cleanr = re.compile('<.*?>')
                    cleantext = re.sub(cleanr, '', raw_html)
                    stopterms = ['&#13;','13#&','&#13','\n','\xa0']
                    querywords = cleantext.split()
                    resultwords  = [word for word in querywords if word.lower() not in stopterms]
                    article_text = ' '.join(resultwords)

            #    elif feed_type is 'BeautifulSoup':

            except: # Main article link either broken or not present in feed
                article_link = None
                article_text = None

            publishedDate = datetimehandler.convertRSSdate(raw_published)

            params = (f[0],source, country, publishedDate, article_title, article_text, article_link)
            sql_insert = """INSERT IGNORE INTO news (news_feed, news_source, news_country, news_date, \
            news_title, news_text, news_link) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_insert,params)


# -----------------------------------------------------------------------------
# ---------------------------------SELENIUM - BS - HANDLER --------------------
# -----------------------------------------------------------------------------    

#def handle_SelBS(source, country, cursor):
    # do stuff

# -----------------------------------------------------------------------------
# ---------------------------------MAIN CODE-----------------------------------
# -----------------------------------------------------------------------------
start_time = datetime.now()

db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
cursor = db.cursor()

cursor.execute("SELECT * FROM sources WHERE sou_type LIKE %s;",("%RSS%"))
sources = cursor.fetchall()

for source in sources: # id, source, country, updated, feeds, type, logo, link
    if source[5][0:3] == 'RSS':
        handle_rss(source[1],source[2],cursor,source[5][4:])
        db.commit()
        
    elif source[5] == 'Selenium-BeautifulSoup':
        handle_SelBS(source[2],source[1],cursor)

    else:
        print("error reading for db:sources")

    today = datetime.now()
    updated_time = today.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPDATE sources SET sou_updated = %s WHERE sou_id = %s;",(updated_time,source[0]))
    db.commit()

db.close()
print("\nRuntime: %s seconds" % (str(datetime.now() - start_time)))