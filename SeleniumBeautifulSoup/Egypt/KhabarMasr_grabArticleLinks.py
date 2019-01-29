# Egypt - Khabar Masr
# http://www.khabarmasr.com

# This code uses Selenium and BeautifulSoup to get all the news article
# links for a given category page (target_url).
# There are multiple pages are links with numbered page buttons at bottom
# Selenium clicks on the 'next' button at the bottom of the page
# then regrabs the page source before passing it to BeautifulSoup

# For the single article scrapes, Newspaper works well

# works really well

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time

opts = Options()
opts.set_headless()

assert opts.set_headless
browser = Firefox(options=opts)
target_url = 'http://www.khabarmasr.com/news/category/1/1'
browser.get(target_url)

page = browser.page_source
soup = BeautifulSoup(page, 'lxml')

page_numbers = soup.find('li', attrs={'class': 'setPage'}).text.strip()
page_numbers.split()[3]

link_cnt = 0
for i in range(1,4):

    main_container = soup.find('div', attrs={'class': 'col-md-8'})

    for a in main_container.find_all('div', "col-md-4"):
        link_cnt += 1
        print(a.find('a')["href"])

    for a in main_container.find_all('div', "col-md-6"):
        link_cnt += 1
        print(a.find('a')["href"])

    try:
        browser.find_element_by_xpath('/html/body/div/div[4]/div/div/div[1]/ul/li[12]/a').click()
        time.sleep(5)
    except NoSuchElementException:
        break

    page = browser.page_source
    soup = BeautifulSoup(page, 'lxml')
    

print("Total links: ", link_cnt)

