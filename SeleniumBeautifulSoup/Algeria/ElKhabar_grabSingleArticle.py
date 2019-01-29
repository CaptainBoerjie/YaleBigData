# Algeria - El Khabar
# https://www.elkhabar.com 

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

def grab(url):
    url = 'https://www.elkhabar.com/press/article/149718/'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('h2', attrs={'id': 'article_title'})
    date_box = soup.find('div', attrs={'class': 'subinfo'})
    article_box = soup.find('div', attrs={'id': 'article_body_content'})

    title = title_box.text.strip()
    date = date_box.text.strip()
    article = article_box.text.strip()

    print(title)
    print(date)
    print(article)