import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import pandas as pd
import json
from OneTimeScrapper import *


class StockNewsScrapper:
    results = []

    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        response = requests.get(url)
        print(' | Status code: %s' % response.status_code)

        return response

    def to_csv(self, df):
        movie_exists = os.path.isfile('s.csv')
        if not movie_exists:
            df.to_csv('s.csv', index=False, mode='a')
        else:
            df.to_csv('s.csv', index=False, header=False, mode='a')

    def parse(self, response):

        content = BeautifulSoup(response, 'lxml')
        titles = [title.text for title in content.find_all('h2', class_='entry-title')]
        links = [link.find('a')['href'] for link in content.find_all('h2', class_='entry-title')]
        dates = [date.text for date in content.find_all('span', class_='meta-date')]
        articles = []
        authors = []

        for link in links:
            res = requests.get(link)
            soup = BeautifulSoup(res.text, 'lxml')
            article_body = ''.join([line.text for line in soup.find('div', class_='entry entry-content').find_all('p')])
            author = soup.find('span', class_='meta-author').text.split('By ')[-1]
            authors.append(author)
            articles.append(article_body)

        df = pd.DataFrame({

            'Titles': titles,
            'Links': links,
            'Dates': dates,
            'Author': authors,
            'Articles': articles
        })
        self.to_csv(df)

    def run(self):

        for page in range(1, 3):
            response = self.fetch('http://www.stockpricetoday.com/stock-news/page/' + str(page) + '/')

            if response.status_code == 200:
                self.parse(response.text)
            else:
                print('Something has gone wrong, skipping to next page')
                continue

            time.sleep(2)


if __name__ == '__main__':
    scraper = StockNewsScrapper()
    scraper.run()
