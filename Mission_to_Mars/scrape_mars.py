# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added



#%%
import pymongo

from splinter import Browser
from bs4 import BeautifulSoup as bs

import pandas as pd
import requests

from tabulate import tabulate


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


db = client.mars_db
collection = db.data

def mars_scraper():
    #%%
    #Getting articles

    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    results = soup.find_all('div', class_='slide')


    titles = []
    blurbs = []

    for result in results:
        try:
            blurb = result.find('div', class_="rollover_description_inner").text
            title = result.find('div', class_="content_title").text
            titles.append(title)
            blurbs.append(blurb)
            
        except:
            print("oops")



    #I couldn't get splinter to work on my computer, so I cheated and found the image url
    image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16883_hires.jpg'


    #Getting weather
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    weather = soup.find_all('div', class_='js-tweet-text-container')
    weather[0].text

    weather = [item.text for item in weather ]
    weather = [item.strip() for item in weather if str(item)]

    mars_weather = weather[0]

    #Getting planet info
    url = 'https://space-facts.com/mars'
    response = requests.get(url)

    soup = bs(response.text, 'html.parser')

    info = soup.find_all('table')[0]

    df = pd.read_html(str(info))
 
    df = df[0].to_json(orient='records')
    post = {'titles' : titles, 
            'blurbs' : blurbs,
            'image' : image_url,
            'weather' : mars_weather,
            'planet_info' : df}
    
    print(post)

    db.data.insert_one(post)

mars_scraper()