from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import datetimehandler


opts = Options()
opts.set_headless()

assert opts.set_headless
browser = Firefox(options=opts)

target_url = 'http://www.elkhabar.com/press/article/2/'
browser.get(target_url)

try:
    print("---entering try---")
    err404 = browser.find_element_by_xpath('/html/body/div/center/div/div[2]/h2')
    page404_cnt += 1
    print("404 found: i = ",i)
    
except NoSuchElementException:
    # page exists, proceed with code

    page = browser.page_source
    soup = BeautifulSoup(page, 'lxml')

    title_box = soup.find('h2', attrs={'id': 'article_title'})
    date_box = soup.find('time', attrs={'class': 'relative_time'}).get('datetime')
    article_box = soup.find('div', attrs={'id': 'article_body_content'})

    title = title_box.text.strip()
    date = date_box.text.strip()
    article = article_box.text.strip()

    print(datetimehandler.convertRSSdate(date))
    print(title)
