import json

import random
import os
from decouple import config
from fastapi import FastAPI
from pymongo import MongoClient  # DataBase Connected Section

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bson import json_util
from fastapi import FastAPI, Body, Request, Query
import uvicorn


app = FastAPI()

MONGO_CLIENT_URL = config("MONGO_CLIENT_URL")

client = MongoClient(MONGO_CLIENT_URL)
data_base = client["product_scraper"]
tables_columns = data_base["products"]




@app.get("/")
def index():
    return {"details": "good"} 


@app.get("/aws-product-scrapper")
def aws_scrapper(url, is_head_less: bool):
    allProxies=[]
    proxyEnv=config("proxies")
    allProxies.append(proxyEnv.split(","))
    for indexProxy in allProxies:
            randomProxy = random.choice(indexProxy)      
    options = Options()
    options.add_argument("--proxy-server={}".format(randomProxy))
    options.headless = is_head_less
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.maximize_window()
    driver.get(url)
    product_title = driver.find_element(By.ID, "title").text
    total_rating = driver.find_element(By.ID, "acrCustomerReviewText").text
    product_rating = driver.find_element(By.ID, 'acrPopover').get_attribute('title')
    store_link = driver.find_element(By.ID, "bylineInfo").get_attribute('href')
    about_item = driver.find_element(By.ID, "feature-bullets").text
    price = driver.find_element(By.XPATH, '//*[@id="availability"]/span').text

    store_url = f"{store_link}"
    driver.get(store_url)
    company_name = driver.find_element(By.CSS_SELECTOR, "h1 > span > span").text

    dict = {

        "product_title": product_title,
        "company_name": company_name,
        "about_item": json.dumps(about_item),
        "price": price,
        "product_rating": product_rating,
        "total_rating": total_rating,
        "store_link": store_url,

    }

    tables_columns.insert_one(dict)

    driver.quit()
    dict['_id'] = str(dict['_id'])

    return {"data": dict}


@app.get("/all-products")
def get_all_records():
    data = []
    for dic in tables_columns.find({}):
        data_load = json.loads(json_util.dumps(dic))
        data.append(data_load)

    return {"data": data}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
