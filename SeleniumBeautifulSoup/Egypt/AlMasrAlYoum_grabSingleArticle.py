# Egypt - Al Masr Al Youm
# https://www.almasryalyoum.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

url = 'https://www.almasryalyoum.com/news/details/1364600'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'lxml')

title_box = soup.find('h1', attrs={'class': 'tit_2'})
date_box = soup.find('div', attrs={'class': 'pinfo'}).find('span')
article_box_group = soup.find('div', attrs={'id': 'NewsStory'}).find_all('p')

title = title_box.text.strip()
date = date_box.text.strip()
article = ''
for p in article_box_group:
    article += p.text.strip()

print(title)
print(date)
print(article)