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
from upload_to_drive import GoogleDrive

# VOI
gd = GoogleDrive()
logfile = 'cme_voi.log'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

URLS = {'AUD_VOI' : 'https://www.cmegroup.com/CmeWS/exp/voiProductDetailsViewExport.ctl?media=xls&tradeDate={yyyymmdd}&reportType=P&productId=37',
        'EUR_VOI' : 'https://www.cmegroup.com/CmeWS/exp/voiProductDetailsViewExport.ctl?media=xls&tradeDate={yyyymmdd}&reportType=P&productId=58',
        'CAD_VOI' : 'https://www.cmegroup.com/CmeWS/exp/voiProductDetailsViewExport.ctl?media=xls&tradeDate={yyyymmdd}&reportType=P&productId=48',
        'GBP_VOI' : 'https://www.cmegroup.com/CmeWS/exp/voiProductDetailsViewExport.ctl?media=xls&tradeDate={yyyymmdd}&reportType=P&productId=42',
        'CHF_VOI' : 'https://www.cmegroup.com/CmeWS/exp/voiProductDetailsViewExport.ctl?media=xls&tradeDate={yyyymmdd}&reportType=P&productId=86',
        'NZD_VOI' : 'https://www.cmegroup.com/CmeWS/exp/voiProductDetailsViewExport.ctl?media=xls&tradeDate={yyyymmdd}&reportType=P&productId=78',
        'JPY_VOI' : 'https://www.cmegroup.com/CmeWS/exp/voiProductDetailsViewExport.ctl?media=xls&tradeDate={yyyymmdd}&reportType=P&productId=69'
        }

headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'upgrade-insecure-requests': '1',

        }
s = requests.Session()

startdate_url = 'https://www.cmegroup.com/CmeWS/mvc/Volume/Total/8122?days=30&isProtected'
j = s.get(startdate_url).json()
startdate = datetime.datetime.strptime(j['vdate'][0]['formattedDate'], '%Y%m%d')
enddate = datetime.datetime.strptime(j['vdate'][-1]['formattedDate'], '%Y%m%d')

try: 
    while startdate <= enddate:
        date = startdate.strftime('%Y%m%d')
        
        if startdate.weekday() >=5 :
            startdate += datetime.timedelta(days=1)
            continue
        
        startdate += datetime.timedelta(days=1)
        
        for key, url in list(URLS.items()):    
            
            url2 = url.format(yyyymmdd = date)
            ext = 'xls'
            fname = f'{key}_{date}.{ext}'
            
            if os.path.exists(fname):
                logger.info(f'File exists: {fname}' )
                continue
            
            r = s.get(url2, verify=False, headers=headers, timeout=30)
            if r.status_code ==200:
                print('downloading file')
                with open(fname, 'wb') as f:
                    f.write(r.content)
                print('uploading file to google drive')
                gd.upload_basic(fname)

            else:
                logger.error(f'Date not exists: {fname}')
except:
    print("Something wrong, kindly check the logs")
    logger.error('Unhandled exception', exc_info=True)
    input("Press any key to continue")
    

