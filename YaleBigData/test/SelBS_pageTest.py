from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


opts = Options()
opts.set_headless()

assert opts.set_headless
browser = Firefox(options=opts)
    
target_url = 'https://www.alayam.com/online/international/60050/News.html'
browser.get(target_url)

try:
    err404 = browser.find_element_by_css_selector('.error')
    print("404 found")
    
except NoSuchElementException:
    # page exists, proceed with code

    #try:
    page = browser.page_source
    soup = BeautifulSoup(page, 'lxml')

    title_box = soup.find('h1', attrs={'itemprop': 'headline'})
    date_box = soup.find('span', attrs={'class': 'datetimefull'})
    if date_box == None:
        date_box = soup.find('div', attrs={'class': 'article-time'})

    article_box = soup.find('div', attrs={'id': 'readerText'})

    if len(date_box.text.strip().split()) > 9:
        date = ' '.join(date_box.text.strip().split()[i] for i in range (2,6))
    else:
        date = date_box.text.strip()

    print(title_box.text.strip())
    print(date)
    #print(article_box.text.strip())

