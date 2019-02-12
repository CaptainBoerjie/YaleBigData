
import pymysql
import requests
import feedparser
import Newspaper_singlearticle

db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
cursor = db.cursor()

cursor.execute("SELECT fee_country,fee_source,fee_link FROM feeds \
    WHERE (fee_id > 43 AND fee_id < 98) OR \
        (fee_id > 154 AND fee_id < 169) OR (fee_id > 180 AND fee_id < 186) OR \
            (fee_id > 286 AND fee_id < 300) OR (fee_id > 339 AND fee_id < 343) OR \
                (fee_id > 365 AND fee_id < 385) OR (fee_id > 391 AND fee_id < 407) OR \
                    (fee_id > 459 AND fee_id < 481) OR (fee_id > 634 AND fee_id < 656);")
feeds = cursor.fetchall()

for f in feeds:
    try: 
        feed = feedparser.parse(f[2])

        print(f[0] + "  :  " + f[1])
        print(feed.entries[0].title)
        print(feed.entries[0].link)
        try:
            print(feed.entries[0].published)
        except:
            print("NO RSS FEED DATE")

        try:
            Newspaper_singlearticle.test_newspaper(feed.entries[0].link)
        except:
            print("NEWSPAPER FAILED")
        
        var = input("--------- press ANY KEY for next feed: ")
        if var != '':
            break

    except:
        print(f[0] + "  :  " + f[1])
        print("NO RSS FEED")

db.close()
