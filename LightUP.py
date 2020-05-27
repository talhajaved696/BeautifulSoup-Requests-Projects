import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import pandas as pd


# response = requests.get('https://www.lightup.com/standard-household-lighting.html')
class BulbScrapper:
    base_url = 'https://www.lightup.com/standard-household-lighting.html?p='

    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        response = requests.get(url)
        print(' | Status code: %s' % response.status_code)

        return response

    def parse(self, response):
        content = BeautifulSoup(response, 'lxml')
        titles = [title.find('a').attrs['title'] for title in content.find_all('h2', {'class': 'product-name'})]
        links = [title.find('a').attrs['href'] for title in content.find_all('h2', {'class': 'product-name'})]
        mpns = [mpn.text for mpn in content.find_all('div', class_='product-list-sku') if 'MPN' in mpn.text]
        skus = [sku.text for sku in content.find_all('div', class_='product-list-sku') if 'SKU' in sku.text]
        features = [tag.find_all('li') for tag in content.find_all('div', class_='desc std')]
        bases = [''.join([base.text for base in feature if "Base:" in base.text]).split(":")[-1] for feature in
                 features]
        wattages = [''.join([wattage.text for wattage in feature if 'Wattage:' in wattage.text]).split(':')[-1].strip() for feature in features]
        watt_eqvs = [
            ''.join([wattage.text for wattage in feature if 'Watt Equivalent:' in wattage.text]).split(':')[-1].strip()
            for feature in features]
        lumens = [''.join([lumen.text for lumen in feature if 'Lumens:' in lumen.text]).split(':')[-1].strip() for
                  feature in features]
        lumens_per_watt = [
            ''.join([lumen.text for lumen in feature if 'Lumens Per Watt:' in lumen.text]).split(':')[-1].strip() for
            feature in features]
        warranties = [
            ''.join([warranty.text for warranty in feature if 'Warranty:' in warranty.text]).split(':')[-1].strip() for
            feature in features]
        extras = [''.join([extra.text for extra in feature if 'Features:' in extra.text]).split(':')[-1].strip() for
                  feature in features]

        df = pd.DataFrame({
            'Title': titles,
            'Link': links,
            'MPN': mpns,
            'SKU': skus,
            'Base': bases,
            'Wattage': wattages,
            'Wattage equivalent': watt_eqvs,
            'Lumens': lumens,
            'Lumens per Watt': lumens_per_watt,
            'Warranty': warranties,
            'Features': extras
        })
        self.to_csv(df)

    def to_csv(self, df):
        movie_exists = os.path.isfile('bulbs.csv')
        if not movie_exists:
            df.to_csv('bulbs.csv', index=False, mode='a')
        else:
            df.to_csv('bulbs.csv', index=False, header=False, mode='a')

    def run(self):
        for page in range(1, 3):
            next_page = self.base_url + str(page)
            response = self.fetch(next_page)

            if response.status_code == 200:
                self.parse(response.text)
            else:
                print('Something has gone wrong, skipping to next page')
                continue

            time.sleep(2)

if __name__ == '__main__':
    scraper = BulbScrapper()
    scraper.run()
# with open('bulbs.html', 'r') as html_file:
#       for line in html_file.read():
#          response += line
