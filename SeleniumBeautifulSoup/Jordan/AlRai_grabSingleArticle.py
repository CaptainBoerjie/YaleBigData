# Jordan - Al Rai
# https://alrai.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

quote_page = 'http://alrai.com/article/10467452/%D9%85%D8%AD%D9%84%D9%8A%D8%A7%D8%AA/%D8%A7%D9%84%D8%B9%D8%A7%D8%B5%D9%85%D8%A9/%D8%A7%D9%84%D8%B5%D9%81%D8%AF%D9%8A-%D9%8A%D9%84%D8%AA%D9%82%D9%8A-%D9%88%D8%B2%D8%B1%D8%A7%D8%A1-%D8%AE%D8%A7%D8%B1%D8%AC%D9%8A%D8%A9-%D9%88%D9%85%D8%B3%D8%A4%D9%88%D9%84%D9%8A%D9%86-%D9%85%D8%B4%D8%A7%D8%B1%D9%83%D9%8A%D9%86-%D9%81%D9%8A-%D8%AF%D8%A7%D9%81%D9%88%D8%B3?rss=1'

page = requests.get(quote_page)
soup = BeautifulSoup(page.content, 'lxml')

title_box = soup.find('div', attrs={'class': 'title-2'})
date_box = soup.find('div', attrs={'class': 'schedule-i'})
article_box = soup.find('div', attrs={'class': 'articleBody'})

title = title_box.text.strip()
date = date_box.text.strip()
article = article_box.text.strip()

print(title)
print(date)
print(article)