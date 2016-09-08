#### The folder contains scrapy project.
#### The most important file is spiders/dmoz_spider.py
#### The work done is
- First go to a site
- Extract the text
- Find the positions where free and trial occurs
- Extract the text 5 positions before and after

and dump the data
## Current Problems:
    - Infinite scraping with sites like twitter
    - Text is included twice if free and promotions have interleaving

To run install scrapy and nltk.
Then run `scrapy crawl dmoz -o items.json`