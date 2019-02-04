# YaleBigData

This is a Big Data project to explore two fields, data science, and Arabic media.

# Current Effort

<b>Week of 3 Feb - 9 Feb</b>
- Currently, working through the main sources list (SourceList.txt) to determine best scraping method.  All sources offer RSS feeds, but some require Newspaper3k (very simple), some require BeautifulSoup (source specific code), and some require Selenium and BeautifulSoup because the RSS format is broken.
- Developing an automated Historic/Archived scraper.  Most of the sources which have iterable article URLs have a <i>sourcename</i>_singleArticleGrab.py file.  The HistoricGrabController.py module will utilize a csv file which holds the available sources with iterable URL's and a min and max numeric article id.  The id number in the URL has a '*' placeholder for easy .split() insertion of the iterated id number.

Additional efforts:
- Learning how to use relative imports as the package file tree grows and code is shared throughout.
- Incorporating exception handling for request exceptions (timeout, connection refused, etc.) to avoid breaking the code and increase automation.

# Weekly Update

## 1 February 2019

- Began scraping archived news articles not available from an RSS feed.  El Haddaf and El Khabar (Algeria) are still running with around 15,000 articles scraped each.
- Finalized, for now, the datetimehandler.py which formats the numerous datetimes from sites.
- Began testing Flask for simple frontside interface

### Issues encountered

- Git is a new tool and the unfamiliarity caused some frustration; most documentation and support on StackOverflow centered around syncing the local repository with the remote and merging remote updates with the local.  Currently, all local changes must take precendence over the remote (GitHub) repository.  "git push -f origin master" is the current method.
- An ongoing issue, but unavoidable, is the slow speed of Selenium/BeautifulSoup scrapes.  Many websites deny GET requests using the requests package and thus require Selenium.  Executing the scrapes of archived and historic articles is very time consuming: code is still scraping two Algerian news sites (~20,000 articles each, so far) with at least 100k left.

# Primary modules

The following are the primary modules currently employed in the package:
- Main.py: Overall controller for scraping.  Accesses the database to iterate through the sources and then pass on to either RSS scraping or Selenium/BeautifulSoup scraping.
- datetimehandler.py: Handles all of the various datetime groups presented by the sources.  The modules has to handle timezone information, numerous Arabic language names, and various combinations.  The code relies on the dateutils package for primary formatting to standard MySQL datetime compliant format.
- <i>sourcename</i>_grabSingleArticle.py: Scrapes an article page from "sourcename" using requests or Selenium and BeautifulSoup.
- <i>sourcename</i>_grabHistoric.py: Grabs all news articles not posted in an RSS feed.  Many newsites reference their articles with a simple numeric URL which makes iterating through the URLs easy.  Other sites designate the URL with the article title which then requires extensive coding with Selenium to "browse" through the archived articles.
- <i>sourcename</i>_grabCategory.py: Almost all news sites organize articles into categories.  This code scrapes articles in a given category page.  The code makes use of Selenium's .click() function to "load more" articles.

# Built With

- POP! OS (Linux)
- Python: coded in VSCode
- MySQL: coded using CLI
