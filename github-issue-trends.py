#/usr/bin/env python

import requests
import json
from pprint import pprint
import configparser


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')

    page = 1
    items_returned = 100

    while items_returned == int(config['github']['items_per_page']):



        r = requests.get( 'https://api.github.com/search/issues?page={}&per_page={}&q={}'.format(page,
                                                                                                config['github']['items_per_page'],
                                                                                                config['github']['query']),
                          auth=(config['github']['user'], config['github']['password']))
        print("Status code {}, page {} items_per_page {}".format(r.status_code, page, config['github']['items_per_page']))



        if r.status_code == 200:
            page+=1

            github_response = json.loads(r.text)

            print("items {}".format(len(github_response['items'])))
            items_returned = len(github_response['items'])

            for item in github_response['items']:

                type = ''
                for lab in item['labels']:
                    if lab['name'] in ['bug', 'feature','enhancement']:
                        type = lab['name']

                print("#{}\t{}\t{}".format(item['number'],item['created_at'],type))


        else:
            items_returned = 0
