import requests
from bs4 import BeautifulSoup
import csv
import time
import pandas as pd
import os
import json


class OneTimeScrapper:


    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://www.zillow.com/new-york-ny/3_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A3%7D%2C%22usersSearchTerm%22%3A%22New%20York%2C%20NY%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.51765986914063%2C%22east%22%3A-73.43825313085938%2C%22south%22%3A40.399446228024196%2C%22north%22%3A41.01095639055632%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22isMapVisible%22%3Afalse%7D', headers=headers)

    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('https://porschevancouver.ca/inventory?page=1', headers=headers, cookies=cookies)
    results = []

    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')

        #print(' | Status code: %s' % response.status_code)

        #return response

    def to_html(self, html, filename):
        file_exists = os.path.isfile(filename)
        if not file_exists:
            with open(filename, 'w', encoding='utf-8') as html_file:
                html_file.write(html)
        else:
            print("File Already Exists.")

    def read_html(self, filename):
        html = ''
        with open(filename, 'r',encoding='utf-8') as html_file:
            for line in html_file.read():
                html += line
        return html

    def to_json(self):
        with open('zillow_rent.json', 'w') as f:
            f.write(json.dumps(self.results, indent=2))

    def parse(self, html):
        print(html)

    def to_csv(self):
        with open('stocks.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

        print('"stocks.csv" has been written successfully!')

    def run(self):

        response = requests.get('http://www.stockpricetoday.com/stock-news/')

        self.to_html(response.text, 'stock.html')
        content = self.read_html('stock.html')
        self.parse(content)


