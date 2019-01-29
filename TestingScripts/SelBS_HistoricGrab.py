from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql

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

for i in range (2,11):
    
    target_url = 'http://www.elkhabar.com/press/article/' + str(i) + '/'
    browser.get(target_url)

    try:
        err404 = browser.find_element_by_xpath('/html/body/div/center/div/div[2]/h2')
        page404_cnt += 1
        print("404 found: i = ",i)
        
    except NoSuchElementException:
        # page exists, proceed with code

        try:
            page = browser.page_source
            soup = BeautifulSoup(page, 'lxml')

            title_box = soup.find('h2', attrs={'id': 'article_title'})
            date_box = soup.find('div', attrs={'class': 'subinfo'})
            article_box = soup.find('div', attrs={'id': 'article_body_content'})

            title = title_box.text.strip()
            date = date_box.text.strip()
            article = article_box.text.strip()

            print(date)
            print(title)

            params = ('','Al Khabar', 'Algeria', date, title, article, url)
            sql_insert = """INSERT IGNORE INTO news (news_feed, news_source, news_country, news_date, \
            news_title, news_text, news_link) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql_insert,params)
            db.commit()

        except:
            deadpage_cnt += 1
            
db.close()

print("Articles added: ", article_cnt)
print("404 pages: ", page404_cnt)
print("Other dead page: ", deadpage_cnt)
print("Total time: ", str(datetime.now() - start_time))