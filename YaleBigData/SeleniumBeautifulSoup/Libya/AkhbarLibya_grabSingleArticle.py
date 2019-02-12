# Jordan - As Sabeel
# https://assabeel.net

# This code requires Selenium because the html is generated by javascript and so
# BS alone is unable to find <html> tags in the source because none have been generated

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import time


def grabPage(url):

    opts = Options()
    opts.set_headless()

    assert opts.set_headless
    browser = Firefox(options=opts)
    browser.get(url)
    time.sleep(10)

    page = browser.page_source
    soup = BeautifulSoup(page, 'lxml')

    title_box = soup.find('h1', attrs={'class': 'post-title'})
    date_box = soup.find('time', attrs={'class': 'post-date'}).get('datetime')
    article_box = soup.find('section', attrs={'class','article-content'}).find_all('p')

    title = title_box.text.strip()
    date = date_box.text.strip()
    
    article = ''
    for a in article_box:
        article += a.text.strip()

    return [title,date,article]

if __name__ == "__main__":

    page = 'www.akhbarlibya.net/arabic-news/10000.html'

    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])