import requests
from bs4 import BeautifulSoup
from decouple import config
import random
import json

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
			# If there is some deal price
			price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

		except:
			price = ""

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
        about = ""
    return about
