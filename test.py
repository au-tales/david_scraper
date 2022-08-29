import json
import time
import random
import os
from decouple import config
from fastapi import FastAPI
from pymongo import MongoClient  # DataBase Connected Section

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.proxy import ProxyType, Proxy #proxy module
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bson import json_util
from fastapi import FastAPI, Body, Request, Query
import uvicorn
import pickle
import requests
from bs4 import BeautifulSoup


# driver.get(url)
# allProxies=[]
# proxyEnv=config("proxies")
# allProxies.append(proxyEnv.split(","))
# for indexProxy in allProxies:
#         proxy_ip = random.choice(indexProxy)


# options = FirefoxOptions()
# options.add_argument('--proxy-server=%s' % proxy_ip)
# # options.binary_location = '/snap/bin/brave'

# options.headless = False
# options.log.level = "trace"


# # set the profile
# myProxy = proxy_ip
# ip, port = myProxy.split(":")

# proxy = Proxy({
#     'proxyType': ProxyType.MANUAL,
#     'httpProxy': myProxy,
#     'ftpProxy': myProxy,
#     'sslProxy': myProxy,
#     'noProxy': '' # set this value as desired
#     })

# # driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
# driver = webdriver.Firefox(executable_path='gecko/geckodriver', options = options, proxy=proxy)
# # driver.implicitly_wait(0.6)
# driver.get('https://www.amazon.com/Belli-Acne-Control-Spot-Treatment/dp/B00I9MZZTC')
# cookies = pickle.load(open("cookies.pkl", "rb"))
# for cookie in cookies:
#     driver.add_cookie(cookie)


HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
URL = "https://www.amazon.com/Belli-Acne-Control-Spot-Treatment/dp/B00I9MZZTC"
webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "lxml")
print(soup)