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
from bs4 import BeautifulSoup
from decouple import config
import random
import json
import requests
from scrape_products import get_title, get_price,get_store_link,get_about_product,get_availability,get_rating, get_review_count,load_browser, is_captcha


app = FastAPI()

MONGO_CLIENT_URL = config("MONGO_CLIENT_URL")

client = MongoClient(MONGO_CLIENT_URL)
data_base = client["product_scraper"]
tables_columns = data_base["products"]


@app.get("/")
def index():
    return {"details": "good"}

@app.get("/aws-product-scrapper")
def aws_scrapper(product_id="B00I9MZZTC"):
    dict = {}

    html = load_browser(product_id)
    soup = BeautifulSoup(html, "lxml")

    if is_captcha(soup):
        html = load_browser(product_id)
        soup = BeautifulSoup(html, "lxml")


    dict = {
        "product_title": get_title(soup),
        "price": get_price(soup),
        "about_item": json.dumps(get_about_product(soup)),
        "product_rating": get_rating(soup),
        "total_rating": get_review_count(soup),
        "availablity": get_availability(soup),
        "store_link":get_store_link(soup),
        "product_id": product_id
    }

    print("------------>", dict)
    try:
        find_object = [x for x in tables_columns.find({'product_id': f"{product_id}"})][0]
        if "_id" in find_object:
            tables_columns.find_one_and_update({'_id': find_object['_id']}, {'$set': dict})
    except IndexError as e:
        tables_columns.insert_one(dict)


    return {"data": dict}


@app.get("/all-products")
def get_all_records():
    data = []
    for dic in tables_columns.find({}):
        data_load = json.loads(json_util.dumps(dic))
        data.append(data_load)

    return {"data": data}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8060, reload=True)
