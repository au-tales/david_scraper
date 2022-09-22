import requests
from bs4 import BeautifulSoup
from decouple import config
import random
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def get_proxy_ip():
    allProxies=[]
    proxyEnv=config("proxies")
    allProxies.append(proxyEnv.split(","))
    for indexProxy in allProxies:
            proxy_ip = random.choice(indexProxy)
    return proxy_ip

def get_title(soup):

	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})

		# Inner NavigatableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip()

		# # Printing types of values for efficient understanding
		# print(type(title))
		# print(type(title_value))
		# print(type(title_string))
		# print()

	except AttributeError:
		title_string = ""

	return title_string

def get_price(soup):
    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()
        except AttributeError:
            try:
                price = soup.find("span", attrs={"class": "a-offscreen"}).string.strip()
            except:
                price=""

    return price


def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating

def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""

    return review_count

def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available

def get_store_link(soup):
    try:
        store_link= soup.find('a', attrs={'id':'bylineInfo'}).get('href')
    except AttributeError:
        store_link=''
    return store_link

def get_about_product(soup):
    try:
        about = soup.find('div', attrs={"id": 'feature-bullets'}).text.strip()
    except AttributeError:
        about = "No discription found"
    return about


def load_browser(product_id, is_headless =  False):
    URL = f"https://www.amazon.com/dp/{product_id}"
    print('proxy_ip is -------->', get_proxy_ip())
    options = Options()
    options.add_argument('--proxy-server=%s' % get_proxy_ip())
    options.headless = is_headless

    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.implicitly_wait(0.6)
    driver.get(URL)
    driver.implicitly_wait(0.6)
    soup = driver.page_source
    driver.quit()
    return soup

def is_captcha(soup):
    try:
        if soup.select('div.a-box-inner > h4')[0].text == 'Enter the characters you see below':
            return True
        else:
            return False
    except Exception as e:
        print("error at captcha", e)
        return False