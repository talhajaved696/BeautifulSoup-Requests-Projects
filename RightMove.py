import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import pandas as pd


# response = requests.get('https://www.lightup.com/standard-household-lighting.html')
class RightMoveScrapper:
    base_url = 'https://www.lightup.com/standard-household-lighting.html?p='

    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        response = requests.get(url)
        print(' | Status code: %s' % response.status_code)

        return response

    def parse(self, response):

        content = BeautifulSoup(response, 'lxml')
        titles = [head.text.replace('\n', '').strip() for head in content.find_all('h2', class_='propertyCard-title')]
        addresses = [address.text.replace('\n', '') for address in
                     content.find_all('address', class_='propertyCard-address')]
        description = [desc.text for desc in content.find_all('span', {'data-test': 'property-description'})]
        prices = [price.text.strip() for price in content.find_all('div', class_='propertyCard-priceValue')]
        dates = [date.text.split(" ")[-1] for date in
                 content.find_all('span', class_='propertyCard-branchSummary-addedOrReduced')]
        sellers = [seller.text.split('by')[-1].strip() for seller in
                   content.findAll('span', {'class': 'propertyCard-branchSummary-branchName'})]
        images = [img['src'] for img in content.find_all('img', {"itemprop": "image"})]

        df = pd.DataFrame({
            'title': titles,
            'address': addresses,
            'description': description,
            'price': prices,
            'date': dates,
            'seller': sellers,
            'image': images,
        })
        self.to_csv(df)

    def to_csv(self, df):
        movie_exists = os.path.isfile('london_property.csv')
        if not movie_exists:
            df.to_csv('london_property.csv', index=False, mode='a')
        else:
            df.to_csv('london_property.csv', index=False, header=False, mode='a')

    def run(self):
        for page in range(0, 2):
            index = page * 24
            response = self.fetch(
                'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E93917&index=' + str(index) +'&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords=')

            if response.status_code == 200:
                self.parse(response.text)
            else:
                print('Something has gone wrong, skipping to next page')
                continue

            time.sleep(2)


if __name__ == '__main__':
    scraper = RightMoveScrapper()
    scraper.run()
