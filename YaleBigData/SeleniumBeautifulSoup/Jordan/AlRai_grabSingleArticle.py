# Jordan - Al Rai
# https://alrai.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('div', attrs={'class': 'title-2'})
    date_box = soup.find('div', attrs={'class': 'col-md-8'}).find('div', attrs={'class': 'schedule-i'})
    article_box = soup.find('div', attrs={'class': 'articleBody'})

    title = title_box.text.strip()
    date = date_box.text.strip()
    article = article_box.text.strip()

    date = ' '.join(date.split()[i] for i in range(2,5))

    return [title,date,article]

if __name__ == "__main__":

    page = 'http://alrai.com/article/10468767/'

    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])

