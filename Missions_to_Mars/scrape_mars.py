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

    #title headline
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # scrap the news title and paragraph
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='rollover_description_inner').text
    mars_info["news_title"] = news_title.strip()
    mars_info["news_p"] = news_p.strip()

    #featured image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # scrap featured image
    div_style = soup.find(class_="carousel_item")['style']
    style = cssutils.parseStyle(div_style)
    image_url = style['background-image']

    #Cut of the '()' and 'url'
    image_url = image_url.replace('url(', '').replace(')', '')

    #added https://www.jpl.nasa.gov to url collected string
    # featured_image_url = print(f"https://www.jpl.nasa.gov{image_url}")
    mars_info["featured_image_url"] = f"https://www.jpl.nasa.gov{image_url}"

    #finding titles of hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    #scrap titles of hemispheres
    title_list = []
    for i in range(0,4):
        title_dic = {}
        title = browser.find_by_css('h3')[i].text
        title_dic['title'] = title
        title_list.append(title_dic)
    
    mars_info["hemi_titles"] = title_list

    return mars_info
 