# Iraq - Az Zamman
# https:// 

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article

import requests
from bs4 import BeautifulSoup

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('h1', attrs={'class': 'entry-title'})
    date_box = soup.find('time', attrs={'class': 'entry-date'})
    article_box = soup.find('div', attrs={'class': 'td-post-content'}).find_all('p', attrs={'style': 'direction: rtl;'})

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

    page = 'https://www.azzaman.com/%d8%b4%d8%b1%d8%b7%d8%a9-%d8%a7%d9%84%d9%86%d8%a7%d8%b5%d8%b1%d9%8a%d8%a9-%d8%aa%d8%b5%d8%b7%d8%a7%d8%af-%d9%85%d8%a8%d8%aa%d9%88%d8%b1-%d8%b3%d8%a7%d9%82%d9%8a%d9%86-%d9%8a%d8%b1%d9%88%d9%91%d8%ac/'

    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])