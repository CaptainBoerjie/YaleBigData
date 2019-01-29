# Egypt - Masrawy
# https://www.mawrawy.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

url = 'https://www.masrawy.com/news/news_offeat/details/2019/1/29/1504648/'

page = requests.get(url)
soup = BeautifulSoup(page.content, 'lxml')

title_box = soup.find('div', attrs={'class': 'articleHeader'}).find('h1')
date_box = soup.find('div', attrs={'class': 'time icon-time'}).find_all('span')[1]
article_box_group = soup.find('div', attrs={'class': 'details'}).find_all('p', attrs={'style': 'direction: rtl;'})

title = title_box.text.strip()
date = date_box.text.strip()
article = ''
for p in article_box_group:
    article += p.text.strip()

print(title)
print(date)
print(article)