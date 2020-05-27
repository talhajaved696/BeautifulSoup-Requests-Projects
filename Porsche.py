import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import pandas as pd

class PorscheScraper:
    base_url = 'https://porschevancouver.ca/inventory?page='
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7',
    }

    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        res = requests.get(url,headers = self.headers)
        print(' | Status code: %s' % res.status_code)
        return res

    def read_html(self, filename):
        html = ''
        with open(filename, 'r') as html_file:
            for line in html_file.read():
                html += line
        return html

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        titles = [title.text.strip() for title in content.find_all('a',class_='vehicle-listing-link')]
        colors = [color.text.strip() for color in content.find_all('div',class_='vehicle-listing-exterior-color')]
        mileage = [mile.text.strip() for mile in content.find_all('div',class_='vehicle-listing-mileage')]
        stocknum = [stk.text.strip() for stk in content.find_all('div',class_='vehicle-listing-stock-number')]
        prices = [price.text.strip() for price in content.find_all('p',class_='vehicle-listing-display-price')]
        images = [image.find('img').attrs['src'] for image in content.find_all('div',class_='vehicle-listing-photo')]

        df = pd.DataFrame({
            'Name': titles,
            'Color': colors,
            'Mileage': mileage,
            'Stock Num': stocknum,
            'Price': prices,
            'Image': images,

        })
        self.to_csv(df)


    def to_csv(self, df):
        movie_exists = os.path.isfile('porsche2.csv')
        if not movie_exists:
            df.to_csv('porsche2.csv', index=False, mode='a',encoding='utf-8')
        else:
            df.to_csv('porsche2.csv', index=False, header=False, mode='a',encoding='utf-8')

    def run(self):

        # response = self.fetch('https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&q=London&search_source=home&radius=0&pn=1')
        #response = self.read_html('porsche.html')
        #self.parse(response)
        for page in range(1, 11):
            next_page = self.base_url + str(page)
            response = self.fetch(next_page)

            if response.status_code == 200:
                self.parse(response.text)
            else:
                print('Something has gone wrong, skipping to next page')
                continue
            time.sleep(2)

        self.to_csv()


if __name__ == '__main__':
    scraper = PorscheScraper()
    scraper.run()

