import lxml.html
import requests
import site_downloader
import database


class Scraping:

    def __init__(self):
        self.urls = ['http://www.espncricinfo.com/big-bash-league-2016-17/engine/series/1023537.html',
                     'http://www.espncricinfo.com/big-bash-league-2015-16/engine/series/897689.html',
                     'http://www.espncricinfo.com/big-bash-league-2014-15/engine/series/756733.html',
                     'http://www.espncricinfo.com/big-bash-league-2013/engine/series/641477.html']
        self.data = []

    def get_data(self):
        for url in self.urls:
            self.source = requests.get(url)
            self.tree = lxml.html.fromstring(self.source.content)
            self.etree = self.tree.xpath('//div[contains(@class, "news-list")]/ul/li[not(child::hr)]')
            for element in self.etree:
                self.match = element.xpath('.//span[@class="potMatchLink"]/a')[0].text_content().strip()
                print(self.match)
                self.date = element.xpath('.//span [@class="potMatchLink"]/following-sibling::text()')[0].strip()
                self.result = element.xpath('.//div[@class="large-5 medium-5 hide-for-small columns arrow-right-data"]/b/text()')[0]
                self.data.append([self.match, self.date, self.result])
        Database = database.Database('data', ('match', 'date', 'result'))
        Database.create_database()
        for item in self.data:
            Database.insert_data(item)
        Database.commit_changes()


Scraping = Scraping()
Scraping.get_data()
