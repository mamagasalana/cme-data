# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 13:41:13 2023

@author: ASUS
"""


import requests
import datetime
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import logging

import glob
import re
from  zip_pdf import myzip
import time

# Settlement

logfile = 'cme_settlement.log'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

import requests


headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'upgrade-insecure-requests': '1',

        }

s = requests.Session()
username = 'API_CMESETTLEMENT'
password = 'tnyN*J97__rq4e6#qgTeM@9M'
s.auth = (username, password)
url = 'https://datamine.cmegroup.com/cme/api/v1/list'
r = s.get(url)
urllist =r.json()['files']

myfiles = []

try:
    urllist2 = []
    for item in urllist:
        url2 = item['url']
        fname = item['fid'] + '.txt'

        if os.path.exists(fname):
            logger.info(f'File exists: {fname}' )
            continue

        urllist2.append(item)

    print(f'{len(urllist2)} items')
    for item in urllist2:
        url2 = item['url']
        fname = item['fid'] + '.txt'

        r = s.get(url2)
        print('downloading file %s' % fname)
        st = time.time()

        if r.status_code ==200:
            print('finish downloading file %s' % fname, "| time taken: ",  time.time() - st )   
            with open(fname, 'wb') as f:
                f.write(r.content)
            
            myfiles.append(fname)
        else:
            logger.error(f'Date not exists: {fname}')

    myzip()
except:
    print("Something wrong, kindly check the logs")
    logger.error('Unhandled exception', exc_info=True)
    input("Press any key to continue")
