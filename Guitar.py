import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import pandas as pd


class GuitarScrapper:
    headers = {
        'authority': 'www.thebassplace.com',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ur;q=0.7',
        'cookie': '_ga=GA1.2.732917449.1588771416; _gid=GA1.2.2070148029.1588892369; _gat=1',
    }


    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        response = requests.get(url, headers=self.headers)
        print(' | Status code: %s' % response.status_code)

        return response

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')
        titles = [', '.join(title.text.split(' – ')[:-2]).strip() for title in
                  content.find_all('h3', class_='product-title')]
        stknum = [''.join(stk.text.split(' – ')[-1]).strip() for stk in content.find_all('h3', class_='product-title')]
        images = [image.attrs['src'] for image in
                  content.find_all('img', class_='attachment-shop_catalog size-shop_catalog wp-post-image')]
        prices = [price.find('span',class_='woocommerce-Price-amount amount').text for price in content.find_all('div', class_='fusion-price-rating')]

        df = pd.DataFrame({
            'Name': titles,
            'Stock Num': stknum,
            'Price': prices,
            'Image': images,

        })
        self.to_csv(df)


    def to_csv(self, df):
        movie_exists = os.path.isfile('guitar1.csv')
        if not movie_exists:
            df.to_csv('guitar1.csv', index=False, mode='a')
        else:
            df.to_csv('guitar1.csv', index=False, header=False, mode='a')

    def read_html(self, filename):
        html = ''
        with open(filename, 'r') as html_file:
            for line in html_file.read():
                html += line
        return html

    def run(self):

        for page in range(1, 3):
            index = page
            response = self.fetch('https://www.thebassplace.com/product-category/basses/4-string/page/'+str(index)+'/')

            if response.status_code == 200:
                self.parse(response.text)
            else:
                print('Something has gone wrong, skipping to next page')
                continue
            time.sleep(2)




if __name__ == '__main__':
    scraper = GuitarScrapper()
    scraper.run()
