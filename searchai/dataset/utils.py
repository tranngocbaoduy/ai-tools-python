import os
import secrets

from PIL import Image
from flask import current_app  
from io import BytesIO 
from datetime import datetime

from searchai.models import DataTrain, AdditionalInfo, InfoAd, FBAdTrain
from searchai import bcrypt 
from searchai.dataset.fbadsspy import ScrapeFBAds
from searchai.dataset.dmmspy import ScrapeDMMSPYAds

# lib to run selenium and analytic data
import os
import time
import json
import lxml
import requests

from bs4 import BeautifulSoup

def get_data_from_fb(keyword): 
    s = ScrapeFBAds("searchai/dataset/chromedriver")
    s.access_data(keyword=keyword, active_status='active')
    s.searchAds(keyword)

def get_data_from_dmmspy(): 
    dmm_spy_ads = ScrapeDMMSPYAds("searchai/dataset/chromedriver")
    dmm_spy_ads.access_data("baoduy19971997@gmail.com","mushroomzz99")
    dmm_spy_ads.DMMSPYget()

def save_picture_author_fb(url):
    # config place, name, size save picture
    random_hex = secrets.token_hex(8)
    picture_fn = random_hex+'.png'
    picture_path = os.path.join(current_app.root_path, 'static/author_fb_pics', picture_fn)

    output_size = (100, 100)

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
 
    img.thumbnail(output_size)

    img.save(picture_path, format='PNG')

    return picture_fn

def save_picture_data(url):
    # config place, name, size save picture
    random_hex = secrets.token_hex(8)
    picture_fn = random_hex+'.png'
    picture_path = os.path.join(current_app.root_path, 'static/train_pics', picture_fn)

    output_size = (350, 350)

    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
 
    img.thumbnail(output_size)

    img.save(picture_path, format='PNG')

    return picture_fn