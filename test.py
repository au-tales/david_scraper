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
from selenium.webdriver.common.proxy import ProxyType, Proxy #proxy module
from selenium.webdriver.chrome.options import Options
from bson import json_util
from fastapi import FastAPI, Body, Request, Query
import uvicorn
import pickle



# driver.get(url)
allProxies=[]
proxyEnv=config("proxies")
allProxies.append(proxyEnv.split(","))
for indexProxy in allProxies:
        proxy_ip = random.choice(indexProxy)


options = Options()
options.add_argument('--proxy-server=%s' % proxy_ip)
options.headless = False


driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
driver.implicitly_wait(0.6)
driver.get('https://www.amazon.com/Belli-Acne-Control-Spot-Treatment/dp/B00I9MZZTC')
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)
