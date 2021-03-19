import csv
import json
import os
import pandas as pd
import requests
import click

# Constants
ROOT = os.path.dirname(os.path.dirname(__file__))

DIR = 'csv_files'

PATH = os.path.join(ROOT, DIR)

os.makedirs(PATH, exist_ok=True)

AUTH_KEY = 'Basic MTU0NzIzOTY2MzowYzdsNjQxaHAy'

URL_DICT = {
    'price-region': '/external/v1/parr/price-regions',
    'sell-price-rules': '/external/v1/parr/seasons-sell',
    'listings': '/external/v1/content/listings',
    'listing-sell-price': '/external/v1/parr/listing-rates-sell'
}

start_date = '2021-06-01'
end_date = '2021-09-30'


class SeaZoneRegion(object):

    def __init__(self):
        self._domain = 'https://ssl.stays.com.br'
        self._headers = {'Authorization': AUTH_KEY}
        self.region_data = []
        self.all_price_rules = []
        self.listings = []
        self.listing_sell_price = []
        print(self.__str__())

    def price_regions_api(self):

        url = self._domain + URL_DICT['price-region']
        click.echo('Fetching price regions...\n')
        try:
            response = requests.get(url=url, headers=self._headers)

            if response.status_code == 200:

                click.echo(click.style('Done!\n', fg='green'))
            else:
                raise ValueError(f"unsuccessful fetch. {response.status_code} error\n")
        except:
            raise ValueError("unsuccessful fetch\n")

        json_response = self._create_json(response.text)
        json_response.pop(1)
        self.region_data = json_response

        file_name = 'region.csv'

        with open(f'{PATH}/{file_name}', 'w') as csvFile:
            csv_writer = csv.writer(csvFile, delimiter=',')
            for region in self.region_data:
                row = [region['name']]
                csv_writer.writerow(row)
            click.echo(f'{file_name} is generated in {PATH}. \n')

    def sell_price_rules(self):
        file_name = 'price_rules.csv'
        click.echo('Fetching sell price rules ...\n')
        with open(f'{PATH}/{file_name}', 'w') as csvFile:
            csv_writer = csv.writer(csvFile, delimiter=',')
            row = ['region', 'rule-name', 'type', 'from', 'to', 'min stay']
            csv_writer.writerow(row)
            for region in self.region_data:
                region_id = region['_id']

                try:
                    data = self._sell_price_rules_request(region_id)
                    self.all_price_rules.append(data)
                except:
                    raise ValueError("unsuccessful fetch\n")

                for item in data:
                    row = [region['name'], item['name'], item['type'], item['from'], item['to'],
                           item['ratePlans'][0]['minStay']]
                    csv_writer.writerow(row)

        click.echo(click.style('Done!\n', fg='green'))
        click.echo(f'{file_name} is generated in {PATH}. \n')

    def get_listings(self):

        url = self._domain + URL_DICT['listings'] + '?limit=50&status=active'
        try:
            click.echo('Fetching all listings...\n')
            data = requests.get(url, headers=self._headers)

        except:
            raise ValueError("unsuccessful fetch\n")

        self.listings = self._create_json(data.text)
        file_name = 'listings.csv'

        with open(f'{PATH}/{file_name}', 'w') as csvFile:
            csv_writer = csv.writer(csvFile, delimiter=',')
            row = ['city', 'street', 'zip', 'subtype', 'status']
            csv_writer.writerow(row)
            for listing in self.listings:
                row = [listing['address']['city'], listing['address']['street'], listing['address']['zip'],
                       listing['subtype'], listing['status']]
                csv_writer.writerow(row)
            click.echo(click.style('Done!\n', fg='green'))
            click.echo(f'{file_name} is generated in {PATH}.\n')

    def get_listing_sell_price(self):
        file_name = 'listing_sell_price.csv'
        with open(f'{PATH}/{file_name}', 'w') as csvFile:
            csv_writer = csv.writer(csvFile, delimiter=',')
            row = ['city', 'region', 'from', 'to', 'price']
            csv_writer.writerow(row)
            click.echo('Fetching listing sell price ... \n')
            for listing in self.listings:
                listing_id = listing['_id']
                data = self._get_listing_sell_price_request(listing_id)
                self.listing_sell_price.append(data)
                for price_list in data:
                    try:
                        listing['address']['region']
                    except:
                        listing['address']['region'] = 'not listed'
                    row = [listing['address']['city'], listing['address']['region'], price_list['from'],
                           price_list['to'], str(price_list['baseRateValue']) + ' R$', ]
                    csv_writer.writerow(row)
        click.echo(click.style('Done!\n', fg='green'))
        click.echo(f'{file_name} is generated in {PATH}. \n')
        df = pd.read_csv(f'{PATH}/{file_name}')
        ans = click.prompt("A dataframe created. Show the head of the dataframe? [y,n] ", type=str)
        if ans.lower() == 'y':
            print(df.head())

    def _get_listing_sell_price_request(self, listing_id):

        url = self._domain + URL_DICT['listing-sell-price'] + f"?listingId={listing_id}&from={start_date}&to={end_date}"
        data = requests.get(url, headers=self._headers)
        return self._create_json(data.text)

    def _sell_price_rules_request(self, region_id):

        url = self._domain + URL_DICT[
            'sell-price-rules'] + '?_idregion=' + region_id + f'&from={start_date}&to={end_date}&status=active'

        response = requests.get(url, headers=self._headers)
        return self._create_json(response.text)

    def _create_json(self, data):
        return json.loads(data)

    def __str__(self):

        return f"API handler:\n" \
               f"main domain: {self._domain}\n"
