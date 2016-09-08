import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import nltk
from bs4 import BeautifulSoup
from freeTrialsCrawler.items import WebInfo
import string
import re
def findConcordanceText(target_word, raw, left_margin=10, right_margin=10):
    raw = re.sub(r'\W+', ' ', raw)
    tokens = nltk.word_tokenize(raw)
    text = nltk.Text(tokens)
    c = nltk.ConcordanceIndex(text.tokens, key=lambda s: s.lower())

    finalText = ""
    for offset in c.offsets(target_word):
        l = offset-10
        r = offset+10
        if offset-10 < 0:
            l=0
        line = ' '.join(tokens[l:r])
        finalText = finalText + ' ' + line
    return finalText




class dmozSpider(CrawlSpider):
  name = 'dmoz'
  start_urls = [
      "http://www.dmoz.org/",
  ]

  def parse(self, response):
      raw = BeautifulSoup(response.body,"lxml").get_text()
      doc1 = findConcordanceText('free',raw)
      doc2 = findConcordanceText('trial', raw)
      if len(doc1) > 10  or len(doc2) > 10:
          item = WebInfo()
          item['link'] = response.url
          item['text'] = doc1+doc2

          yield item

      for link in LinkExtractor(allow=()).extract_links(response):
          yield scrapy.Request(link.url, callback=self.parse_dir_contents)

  def parse_dir_contents(self, response):
      raw = BeautifulSoup(response.body,"lxml").get_text()
      doc1 = findConcordanceText('free',raw)
      doc2 = findConcordanceText('trial', raw)
      if len(doc1) > 10  or len(doc2) > 10:
          item = WebInfo()
          item['link'] = response.url
          item['text'] = doc1+doc2

          yield item

      for link in LinkExtractor(allow=()).extract_links(response):
          yield scrapy.Request(link.url, callback=self.parse_dir_contents)

