# Egypt - Al Wafd
# https://alwafd.news 

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

quote_page = 'http://www.khabarmasr.com/news/get_news/2486217/%D9%85%D8%AD%D9%85%D8%AF-%D8%B9%D8%B2-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8-%D8%B9%D9%86-%D8%A3%D9%88%D9%84-%D9%84%D9%82%D8%A7%D8%A1-%D9%85%D8%B9-%D8%A2%D9%8A%D8%AA%D9%86-%D8%B9%D8%A7%D9%85%D8%B1:-%D8%B5%D8%AF%D9%81%D8%A9-%D9%81%D9%8A-%D9%85%D8%B3%D9%84%D8%B3%D9%84-%D8%A7%D9%84%D8%B3%D8%A8%D8%B9-%D9%88%D8%B5%D8%A7%D9%8A%D8%A7'

page = requests.get(quote_page)
soup = BeautifulSoup(page.content, 'lxml')

title_box = soup.find('div', attrs={'class': 'div_name_cat_title'})
date_box = soup.find('div', attrs={'class': 'news_text'}).find('small')
article_box = soup.find('div', attrs={'class': 'news_text'}).find_all('p')

article = ''
for a in article_box:
    article += a.text

title = title_box.text.strip()
date = date_box.text.strip()
#article = article_box.strip()

print(title)
print(date)
print(article)