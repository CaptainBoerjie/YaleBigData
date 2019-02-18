# Egypt - Masrawy
# https://www.masrawy.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('div', attrs={'class': 'articleHeader'}).find('h1')
    date_box = soup.find('div', attrs={'class': 'time icon-time'}).find_all('span')[1]
    article_box_group = soup.find('div', attrs={'class': 'details'}).find_all('p', attrs={'style': 'direction: rtl;'})

    try:
        title = title_box.text.strip()
        date = date_box.text.strip()
        article = ''
        for p in article_box_group:
            article += p.text.strip()
        return [title,date,article]

    except AttributeError as e:
        return([None,None,None])

if __name__ == "__main__":

    page = 'https://www.masrawy.com/news/news_egypt/details/2019/2/15/1514740/'

    output = grabPage()
    for o in range (0,len(output)):
        print(output[o])