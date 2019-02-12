# Bahrain - Al Ayam
# https://www.alayam.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

from bs4 import BeautifulSoup
import requests

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('h1', attrs={'itemprop': 'headline'})
    date_box = soup.find('span', attrs={'class': 'datetimefull'})
    if date_box is None:
        date_box = soup.find('div', attrs={'class': 'article-time'})
    article_box = soup.find('div', attrs={'id': 'readerText'})
    if article_box is None:
        try:
            article_box = soup.find('div', attrs={'id': 'readerText'}).find_all('div')
            article = ''
            for a in article_box:
                article += a.text
        except:
            article = None
    else:
        article = article_box.text.strip()

    try:
        title = title_box.text.strip()
        date = date_box.text.strip()
        if len(date.split()) > 6:
            date = ' '.join(date.split()[i] for i in range(3,6))
        return [title,date,article]
    except AttributeError as e:
        return([None,None,None])

if __name__ == "__main__":

    page = 'https://www.alayam.com/online/international/406347/News.html'
    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])

"""
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


def grabPage(url):

    opts = Options()
    opts.set_headless()

    assert opts.set_headless
    browser = Firefox(options=opts)
    browser.get(url)

    page = browser.page_source
    soup = BeautifulSoup(page, 'lxml')
"""