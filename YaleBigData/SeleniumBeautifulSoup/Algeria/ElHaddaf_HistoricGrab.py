from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql
import datetimehandler

start_time = datetime.now()

opts = Options()
opts.set_headless()

assert opts.set_headless
browser = Firefox(options=opts)

page404_cnt = 0
article_cnt = 0
deadpage_cnt = 0

db = pymysql.connect("localhost","root","pumpkin","ScrapeDB")
cursor = db.cursor()

for i in range (75740,139102):
    
    target_url = 'http://www.elheddaf.com/article/detail?id=' + str(i)
    browser.get(target_url)

    try:
        err404 = browser.find_element_by_css_selector('.error')
        page404_cnt += 1
        print("404 found: i = ",i)
        
    except NoSuchElementException:
        # page exists, proceed with code

        #try:
        page = browser.page_source
        soup = BeautifulSoup(page, 'lxml')

        title_box = soup.find('div', attrs={'id': 'detail_head'}).find('div', attrs={'class': 'right_area'}).find('h1')
        date_box = soup.find('div', attrs={'class': 'post_bare'}).find('span', attrs={'class': 'time'})
        article_box = soup.find('div', attrs={'id': 'post_core'}).find_all('p')

        title = title_box.text.strip()
        date = date_box.text.strip()
        article = ''
        for a in article_box:
            article += a.text.strip()

        push_date = datetimehandler.convertRSSdate(date)

        params = ('http://www.elheddaf.com/article/detail?id=','Al Haddaf', 'Algeria', push_date, title, article, target_url)
        sql_insert = """INSERT IGNORE INTO news (news_feed, news_source, news_country, news_date, \
        news_title, news_text, news_link) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql_insert,params)
        db.commit()

        article_cnt += 1

        print(push_date)
        print(title)

        #except:
        #    deadpage_cnt += 1
            
db.close()

print("Articles added: ", article_cnt)
print("404 pages: ", page404_cnt)
print("Other dead page: ", deadpage_cnt)
print("Total time: ", str(datetime.now() - start_time))
