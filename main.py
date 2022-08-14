import json
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from pymongo import MongoClient  # DataBase Connected Section
client = MongoClient(os.environ.get("mongodbUrl"))
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from bson import json_util
mydb = client['scrape']
app = FastAPI()

mycol = mydb["data"]
@app.get("/")
def getItems(url):

    driver=webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get(url)
    title=driver.find_element(By.ID,"title").text
    total_rating = driver.find_element(By.ID,'acrCustomerReviewText').text
    company_name = driver.find_element(By.ID,'bylineInfo').text
    about_item = driver.find_element(By.ID,'feature-bullets').text
    price=driver.find_element(By.XPATH,'//*[@id="availability"]/span').text

    dict={
        "Product Title":title,
        "Total Rating":total_rating,
        "Company Name":company_name,
        "About Item":about_item,
        "Price":price
        }


    mydb = client['scrape']
    mycol = mydb["data"]
    mycol.insert_one(dict)

    driver.quit()

    resData=[]
    for dic in mycol.find({}):
             data_load = json.loads(json_util.dumps(dic))
             resData.append(data_load)
            
    return {"Scrape Data":resData}
    


        
        
        
   