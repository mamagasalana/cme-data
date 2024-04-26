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
from lxml import html
import zipfile
import shutil
import time
# import chromedriver_autoinstaller

# import change_chromedriver_js
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from selenium.webdriver.chrome.service import Service

# from selenium_stealth import stealth

# chromedriver_autoinstaller.download_chromedriver()
# change_chromedriver_js.edit_chromedriver()

s = requests.Session()
headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'upgrade-insecure-requests': '1',

        }
current_directory = os.path.dirname(os.path.abspath(__file__))
chromepath= os.path.join(current_directory, "chromedriver.exe")


def extract_version(output):
    try:
        google_version = ''
        for letter in output[output.rindex('DisplayVersion    REG_SZ') + 24:]:
            if letter != '\n':
                google_version += letter
            else:
                break
        return(google_version.strip())
    except TypeError:
        return

stream = os.popen('reg query "HKLM\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Google Chrome"')
output = stream.read()
google_version = extract_version(output)

def update_chromedriver():
    url = 'https://googlechromelabs.github.io/chrome-for-testing'
    
    r = s.get(url, headers=headers)
    tree = html.fromstring(r.content)
    x1 = '//section[@id="stable"]//code[contains(text(), "chromedriver-win64.zip")]'
    new_chrome_url = tree.xpath(x1)[0].text
    current_version = new_chrome_url.split('/')[-3].split('.')[0]

    if int(current_version) > int(google_version.split('.')[0]):
        return
    
    fout = new_chrome_url.split('/')[-1].replace('.zip', f'_v{current_version}.zip')
    fout = os.path.join(current_directory, fout)

    if not os.path.exists(fout):
        r = s.get(new_chrome_url, headers=headers)
        with open(fout, 'wb') as ifile:
            ifile.write(r.content)
    
        # extract zip
        with zipfile.ZipFile(fout, 'r') as zip_ref:
            for f in zip_ref.namelist():
                if 'chromedriver.exe' in f:
                    f2 = zip_ref.extract(f, current_directory)
                    shutil.move(f2, chromepath)

        print('Done')

update_chromedriver()


def launch_driver(folder=None):
    #prevent anti-bot guide
    #https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html
    
    # # selenium-wire proxy settings
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    # capa["unexpectedAlertBehaviour"] = "accept"
    options = webdriver.ChromeOptions()
    # # options.add_argument("--incognito") 
    # # options.add_argument('--ignore-ssl-errors=yes')
    # # options.add_argument('--ignore-certificate-errors')
    # #prevent anti-bot 
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    chromeprofile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clone chrome profile")
    if not os.path.exists(chromeprofile):
        os.makedirs(chromeprofile)
    
    options.add_argument('--user-data-dir=' +chromeprofile)
    
    if folder:
        prefs = {   'download.default_directory' : folder,
                    "download.prompt_for_download": False,
                    "download.directory_upgrade": True,
                    "plugins.always_open_pdf_externally": True}
        options.add_experimental_option('prefs', prefs)
    service = Service(executable_path=chromepath, desired_capabilities=capa) 
    driver = webdriver.Chrome(service=service, options=options)
    # stealth(driver,
    #         languages=["en-US", "en"],
    #         vendor="Google Inc.",
    #         platform="Win32",
    #         webgl_vendor="Google Inc. (Intel)",
    #         renderer="ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
    #         fix_hairline=True
    #         )
    # driver.maximize_window()
    return driver

driver= launch_driver()

# Settlement
gd = GoogleDrive()
logfile = 'etoro.log'
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

file_handler = logging.FileHandler(logfile)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

URLS = {'etoro' : 'https://www.etoro.com/sapi/insights/insights/uniques',
        }





startdate = datetime.datetime.now() - datetime.timedelta(days=12)
enddate = datetime.datetime.now()

try: 
    date =  datetime.datetime.now().strftime('%Y%m%d')
        
    for key, url in list(URLS.items()):    
        
        # ext = url2.split('.')[-1]

        fname = f'{key}_{date}.json'
        
        if os.path.exists(fname):
            logger.info(f'File exists: {fname}' )
            continue
        
        driver.get(url)
        count = 0

        while True:
            x1 = '//pre'
            e1 = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, x1)))
            if ']' in e1.text:
                break
            time.sleep(1)
            count +=1

            if count >= 60:
                break
            
        print('downloading file')
        with open(fname, 'w') as f:
            f.write(e1.text)
        print('uploading file to google drive')
        gd.upload_basic(fname)
        driver.quit()

except:
    print("Something wrong, kindly check the logs")
    logger.error('Unhandled exception', exc_info=True)
    input("Press any key to continue")
    


