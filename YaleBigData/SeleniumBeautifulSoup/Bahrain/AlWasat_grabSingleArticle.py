# Bahrain - Al Wasat News
# https://www.alwasatnews.com

# This code uses BeautifulSoup to grab the title, article date, and article text from
# a single article


from bs4 import BeautifulSoup
import requests

def grabPage(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    title_box = soup.find('h1', attrs={'itemprop': 'headline'})
    date_box = soup.find('span', attrs={'class': 'datetimefull'})
    article_box = soup.find('div', attrs={'id': 'readerText'}).find_all('div')

    try:
        article = ''
        for a in article_box:
            article += a.text
        title = title_box.text.strip()
        date = date_box.text.strip()
        return [title,date,article]
    except AttributeError as e:
        return([None,None,None])

if __name__ == "__main__":

    page = 'https://www.alayam.com/online/international/778215/News.html'
    output = grabPage(page)
    for o in range (0,len(output)):
        print(output[o])