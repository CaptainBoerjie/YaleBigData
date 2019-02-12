# Egypt - Khabar Masr
# https://www.khabarmasr.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('div', attrs={'class': 'div_name_cat_title'})
    date_box = soup.find('div', attrs={'class': 'news_text'}).find('small')
    article_box = soup.find('div', attrs={'class': 'news_text'}).find_all('p')

    article = ''
    for a in article_box:
        article += a.text

    title = title_box.text.strip()
    date = date_box.text.strip()

    return [title,date,article]

if __name__ == "__main__":

    page = 'http://www.khabarmasr.com/news/get_news/2486217/'
    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])