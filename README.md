# YaleBigData

This is a Big Data project to explore two fields, data science, and Arabic media.

# Current Effort

- Building out the web framework.  The current code (within the Flask directory) is rudimentary and only displays current database statistics.
- Incorporating multiprocessing in the historic scraper to scrape all the iterable sources instead of one by one (see 17 February update).

Addition efforts:
- Learning how to use relative imports as the package file tree grows and code is shared throughout.
- Incorporating exception handling for request exceptions (timeout, connection refused, etc.) to avoid breaking the code and increase automation.

# Weekly Update

## 17 February 2019

- Current article count around 1.4 million.  Between daily update scrapes and ongoing historic scraping, the database adds 200-250 thousand a day.
- Began building out the basic web framework with Flask.  The current code just displays the most recent database statistics.
- The statistics are gathered using PeriodicStatistics.py which outputs to PeriodicStatistics.csv
- Finally, tested code for scraping historic articles using multiprocessing.  There is a new database table which holds all the easily iterable news sources (~60).  Up till now, each source has been processed separated and entirely before moving to the next.  This is not a good method because some sources take several days (hundreds of thousands of historic articles) which will make for misleading results when analysis testing begins and several sources' historic articles are not yet scraped.  With the multiprocessing code, tranches of sources will spin up separate asynchronous processes to scrape 500-1000 articles each before ending and starting the next process.  This method will ensure a gradual scraping of all historic articles across a wide array of sources and is extendable as new sources are added.

### Issues Encountered

- Not many issues this week, just coding learning curve with asynchronous multiprocessing (can't pass a database cursor to a subprocess).

## 10 February 2019

- Finalized HistoricGrabController.py which handles scraping for all sources which allow for easily iterable URLs.  Historic scraping has rapidly increased the size of DB to <b>~600,000</b> articles.
-- Developing an automated Historic/Archived scraper.  Most of the sources which have iterable article URLs have a <i>sourcename</i>_singleArticleGrab.py file.  The HistoricGrabController.py module will utilize a csv file which holds the available sources with iterable URL's and a min and max numeric article id.  The id number in the URL has a '*' placeholder for easy .split() insertion of the iterated id number.
- Continued working on Main.py which is the controller for regular daily scraping.  The final section to add is just the Selenium-BeautifulSoup function which relies on the subcode for each of the sources.
- Work continues on the master datetimehandler.py code to deal with the endless datetime permutations.

### Issues Encountered

- A single source Bahrain:Al Ayam changes the datetime format from article to article sometimes including Arabic, Islamic, and Gregorian (all in Arabic language) dates in a single date line.  Additionally, for segments of tens or hundreds of articles, the date will be badly formatted without spaces between some of the digits and numbers which complicates simple .split() operations for parsing a date.
- Currently, Main.py has a mystery error wherein the RSS function exits before the last if/else segment thus never pushing the scraped article to the DB.  Neither the if or else segments are entered and no exception or error is thrown leading to some confusion as to the problem.

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
- HistoricController.py: Handles the historic/archived scraping.
- PeriodicStatistics.py: Grabs daily statistics from the database and outputs to a csv file which is displayed through the Flask web framework.
- <i>sourcename</i>_grabSingleArticle.py: Scrapes an article page from "sourcename" using requests or Selenium and BeautifulSoup.
- <i>sourcename</i>_grabHistoric.py: Grabs all news articles not posted in an RSS feed.  Many newsites reference their articles with a simple numeric URL which makes iterating through the URLs easy.  Other sites designate the URL with the article title which then requires extensive coding with Selenium to "browse" through the archived articles.
- <i>sourcename</i>_grabCategory.py: Almost all news sites organize articles into categories.  This code scrapes articles in a given category page.  The code makes use of Selenium's .click() function to "load more" articles.

# Built With

- POP! OS (Linux)
- Python: coded in VSCode
- MySQL: coded using CLI
