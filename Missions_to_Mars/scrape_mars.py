# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import pymongo
import cssutils
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_info = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # scrap the news title and paragraph
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='rollover_description_inner').text
    mars_info["news_title"] = news_title.strip()
    mars_info["news_p"] = news_p.strip()

    # mars_info["price"] = soup.find("span", class_="result-price").get_text()
    # mars_info["hood"] = soup.find("span", class_="result-hood").get_text()

    return mars_info
 