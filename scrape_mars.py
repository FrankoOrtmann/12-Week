import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd
from flask import Flask, render_template, redirect
import pymongo


def init_browser():
    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    mars_data = {}    
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    title = soup.find('div', class_="content_title").text
    teaser_text = soup.find('div', class_="rollover_description_inner").text
    mars_data['news_title'] = title
    mars_data['news_teaser'] = teaser_text

    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    soup = bs(browser.html, 'html.parser')
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://jpl.nasa.gov"+image
    mars_data['featured_image_url'] = featured_image_url
    
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize").text
    mars_data['weather'] = mars_weather

    # browser = init_browser()
    executable_path = {'executable_path' : 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://space-facts.com/mars/"
    temp = pd.read_html(url,header=1)
    mars_df=pd.DataFrame(temp[0])
    mars_df.columns=['Description','Value']
    mars_df=mars_df.set_index("Description")
    mars_info = mars_df.to_html(classes='mars_info')
    mars_info =mars_info.replace('\n', ' ')
    mars_data['info'] = mars_info

    # # browser = init_browser()
    # executable_path = {'executable_path' : 'chromedriver'}
    # browser = Browser('chrome', **executable_path, headless=False)
    # url = 'http://web.archive.org/web/20181114171728/https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # browser.visit(url)
    # html = browser.html
    # soup = bs(html, 'html.parser')

    hemisphere_image_urls = []
    hemisphere_links = soup.find_all('div', class_='item')
    starter_url = 'http://web.archive.org'

    for a in hemisphere_links:
        time.sleep (3)
        title = a.find('h3').text
        scraped_url = a.find('a', class_='itemLink product-item')['href']
        # browser = init_browser()
        executable_path = {'executable_path' : 'chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(starter_url + scraped_url)
        hemisphere_soup = bs(browser.html, 'html.parser')
        part_img_url = hemisphere_soup.find('img', class_='wide-image')['src']
        img_url = starter_url + part_img_url
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls
    return mars_data

# app = Flask(__name__)
# conn = 'mongodb://localhost:27017'
# client = pymongo.MongoClient(conn)
# db = client.mars_db
# collection = db.mars_db
# collection.insert_one(mars_data)

# results = db.mars_db.find()
# print(results)