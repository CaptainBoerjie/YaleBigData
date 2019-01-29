# Morocco - Maghress
# https://www.maghress.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup
import pymysql

def main(quote_page):
        
    quote_page = 'https://www.maghress.com/alittihad/2082123'

    page = requests.get(quote_page)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('span', attrs={'class': 'articletitle'})
    date_box = soup.find('span', attrs={'class': 'articlenewspaper'})
    article_box = soup.find_all('span', attrs={'class': 'articlecontent'})

    title = title_box.text.strip()
    date = date_box.text.strip()
    article = ''
    for a in article_box:
        article += a.text.strip()

    print(title)
    print(date)
    print(article)

if __name__ == "__main__":
    main(sys.argv[1])