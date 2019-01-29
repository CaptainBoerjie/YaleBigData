# Egypt - Al Ayam
# https://www.alayam.com

# This code uses BeautifulSoup to grab the title and article text from
# a single article

import requests
from bs4 import BeautifulSoup

quote_page = 'https://alwafd.news/%D8%A3%D8%AE%D8%A8%D8%A7%D8%B1-%D9%88%D8%AA%D9%82%D8%A7%D8%B1%D9%8A%D8%B1/2202325-%D9%81%D9%8A-%D8%AD%D8%B2%D8%A8-%D8%A7%D9%84%D9%88%D9%81%D8%AF-%D9%85%D9%88%D8%A7%D8%B7%D9%86%D9%88%D9%86-%D9%8A%D8%B3%D8%A3%D9%84%D9%88%D9%86-%D9%88%D8%B2%D9%8A%D8%B1-%D8%A7%D9%84%D8%AA%D9%85%D9%88%D9%8A%D9%86-%D8%B9%D9%86-%D8%A8%D8%B7%D8%A7%D9%82%D8%A7%D8%AA-%D8%A7%D9%84%D8%AF%D8%B9%D9%85'

page = requests.get(quote_page)
soup = BeautifulSoup(page.content, 'lxml')

title_box = soup.find('h1', attrs={'itemprop': 'headline'})
date_box = soup.find('span', attrs={'class': 'date date-time rtl'})
article_box = soup.find('div', attrs={'class': 'details'})

title = title_box.text.strip()
date = date_box.text.strip()
article = article_box.text.strip()

print(title)
print(date)
print(article)