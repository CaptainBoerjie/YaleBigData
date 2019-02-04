# This code will control the historic and archived article scrapes.  It will 
# handle timeout exceptions and maintain the position of the last scraped
# article.
# As an example, Algeria's El Heddaf newspaper formats the article URLs as such:
# http://www.elheddaf.com/article/detail?id=0000000
# The id number '00000000' is a unique identifier for the article.
# For websites with similar formats, it is simple to iterate through the articles
# and scrape.

# CSV file for sources capable of iterative scraping named HistoricGrabList.csv

import csv

with open('HistoricGrabList.csv','r') as grablist:
    spamreader = csv.reader(grablist)
    for row in spamreader:
        print(row)





