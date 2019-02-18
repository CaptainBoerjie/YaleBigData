# Kuwait - Al Watan
# https://alwatan.kuwait.tt

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('div', attrs={'id': 'divMainTitle'}).find('font')
    date_box = soup.find('font', attrs={'class': 'WriterLink','style':'direction:ltr;'})
    article_box = soup.find('font', attrs={'id': 'divArtContent'})

    try:
        article = article_box.text.strip()
        title = title_box.text.strip()
        date = date_box.text.strip()
        return [title,date,article]

    except AttributeError as e:
        return([None,None,None])

if __name__ == "__main__":

    page = 'http://www.khabarmasr.com/news/get_news/2486217/'
    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])