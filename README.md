# YaleBigData

This is a Big Data project to explore two fields, data science, and Arabic media.

# Current Effort

Currently, working through the main sources list (SourceList.txt) to determine best scraping method.  All sources offer RSS feeds, but some require Newspaper3k (very simple), some require BeautifulSoup (source specific code), and some require Selenium and BeautifulSoup because the RSS format is broken.

Addition efforts:
- Learning how to use relative imports as the package file tree grows and code is shared throughout.
- Continuing to clean the existing database of NULL fields, broken links, and missing published dates.

# Weekly Update

## 1 February 2019

- Began scraping archived news articles not available from an RSS feed.  El Haddaf and El Khabar (Algeria) are still running with around 15,000 articles scraped each.
- Finalized, for now, the datetimehandler.py which formats the numerous datetimes from sites.
- Began testing Flask for simple frontside interface

# Primary modules

The following are the primary modules currently employed in the package:
- Main.py: Overall controller for scraping.  Accesses the database to iterate through the sources and then pass on to either RSS scraping or Selenium/BeautifulSoup scraping.
- datetimehandler.py: Handles all of the various datetime groups presented by the sources.  The modules has to handle timezone information, numerous Arabic language names, and various combinations.  The code relies on the dateutils package for primary formatting to standard MySQL datetime compliant format.
- <source>_grabSingleArticle.py: 
- <source>_grabHistoric.py:
- <source>_grabCategory.py:

# Built With

- POP! OS (Linux)
- Python: coded in VSCode
- MySQL: coded using CLI
