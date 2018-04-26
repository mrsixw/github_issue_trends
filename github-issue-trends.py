#/usr/bin/env python

import requests
import json
from pprint import pprint
import configparser
from datetime import datetime, timedelta

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('config.ini')

    page = 1
    items_returned = 100

    issues = []

    weeks = [
        "01/10/2017",
        "08/10/2017",
        "15/10/2017",
        "22/10/2017",
        "29/10/2017",
        "05/11/2017",
        "12/11/2017",
        "19/11/2017",
        "26/11/2017",
        "03/12/2017",
        "10/12/2017",
        "17/12/2017",
        "24/12/2017",
        "31/12/2017",
        "07/01/2018",
        "14/01/2018",
        "21/01/2018",
        "28/01/2018",
        "05/02/2018",
        "12/02/2018",
        "19/02/2018",
        "26/02/2018",
        "05/03/2018",
        "12/03/2018",
        "19/03/2018",
        "26/03/2018",
        "02/04/2018",
        "09/04/2018",
        "16/04/2018",
        "23/04/2018",
        ]

    while items_returned == int(config['github']['items_per_page']):



        r = requests.get( 'https://api.github.com/search/issues?page={}&per_page={}&q={}'.format(page,
                                                                                                config['github']['items_per_page'],
                                                                                                config['github']['query']),
                          auth=(config['github']['user'], config['github']['password']))
        #print("Status code {}, page {} items_per_page {}".format(r.status_code, page, config['github']['items_per_page']))



        if r.status_code == 200:
            page+=1

            github_response = json.loads(r.text)

            #print("items {}".format(len(github_response['items'])))
            items_returned = len(github_response['items'])

            for item in github_response['items']:

                type = ''
                for lab in item['labels']:
                    if lab['name'] in ['bug', 'feature','enhancement']:
                        type = lab['name']

                #print("#{}\t{}\t{}\t{}".format(item['number'],
                 #                               type,
                  #                              item['created_at'],
                   #                             item['closed_at']))

                issues.append(item)


        else:
            items_returned = 0


    count_dict = {}

    for week in weeks:
        week_ending = datetime.strptime(week,"%d/%m/%Y")
        week_start = week_ending - timedelta(days=7)
        print ("{} {}".format(week_start,week_ending))

        count_dict[week] = {'bug':0, 'feature':0, 'enhancement':0,'unknown':0}

        for issue in issues:
            type = 'unknown'
            for lab in issue['labels']:
                if lab['name'] in ['bug', 'feature', 'enhancement']:
                    type = lab['name']


            issue_open = datetime.strptime(issue['created_at'],"%Y-%m-%dT%H:%M:%SZ")
            if issue['closed_at'] != None:
                issue_closed = datetime.strptime(issue['closed_at'],"%Y-%m-%dT%H:%M:%SZ")
            else:
                issue_closed = None



            print("\t{}\t{}\t{}\t{}".format(issue['number'], type, issue_open, issue_closed))


            if issue_open > week_ending:
                # not open in this week, so skip
                continue
            else:
                if issue_closed != None and issue_closed < week_start:
                    #not in this week
                    continue
                else:
                    count_dict[week][type] += 1


    print (count_dict)


    for key, val in count_dict.items():
        print("{}\t{}\t{}".format(key, val['bug'], val['enhancement']))