import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import pandas as pd

class ZooplaScraper:
    base_url = 'https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&q=London&search_source=home&radius=0&pn='

    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        res = requests.get(url)
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
        cards = content.find_all('div', class_='listing-results-wrapper')
        # tags = card.find_all('a')
        titles = [card.find('a',{'style': 'text-decoration:underline;'}).text for card in cards]
        addresses = [card.find('a', {'class': 'listing-results-address'}).text for card in cards]
        desc = [card.find('p').text.strip() for card in cards]
        date = [card.find_all('small')[1].text.replace('\n','').split('Listed on')[1].split('by')[0].strip() for card in cards]
        price = [''.join(card.find('a', {'class': 'listing-results-price'}).text.replace('\n','').strip().split(' ')[0]) for card in cards]
        phone = [card.find('span', {'class': 'agent_phone'}).text.strip() for card in cards]
        image = [card.find('img').attrs['data-src'] for card in cards]

        df = pd.DataFrame({
            'title': titles,
            'address': addresses,
            'description': desc,
            'price': price,
            'date': date,
            'phone': phone,
            'image': image,
        })
        self.to_csv(df)

    def to_csv(self, df):
        movie_exists = os.path.isfile('zoopla.csv')
        if not movie_exists:
            df.to_csv('zoopla.csv', index=False, mode='a')
        else:
            df.to_csv('zoopla.csv', index=False, header=False, mode='a')

    def run(self):

        # response = self.fetch('https://www.zoopla.co.uk/for-sale/property/london/?identifier=london&q=London&search_source=home&radius=0&pn=1')
        for page in range(1, 3):
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
    scraper = ZooplaScraper()
    scraper.run()
