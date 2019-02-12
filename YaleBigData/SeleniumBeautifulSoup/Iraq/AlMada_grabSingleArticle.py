# Iraq - Al Mada
# https://almadapaper.net/

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('header', attrs={'class': 'article__head'}).find('h1')
    date_box = soup.find('div', attrs={'class': 'article__bar-aside'}).find('span', attrs={'class': 'text-en'})
    article_box = soup.find('div', attrs={'class': 'article__entry'}).find_all('p', attrs={'style': 'text-align: justify;'})

    try:
        title = title_box.text.strip()
        date = date_box.text.strip()
        article = ''
        for a in article_box:
            article += a.text.strip()

        return [title,date,article]
    except AttributeError as e:
        return([None,None,None])

if __name__ == "__main__":

    page = 'https://almadapaper.net/Details/216314/'

    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])

        