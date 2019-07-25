import os
import secrets
import requests

from PIL import Image
from flask import current_app  
from io import BytesIO 
from searchai.models import DataTrain
from searchai import bcrypt 
from datetime import datetime

# lib to run selenium and analytic data
import os
import time
import json
import lxml
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#libs compare two string
from difflib import SequenceMatcher
import jellyfish

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

def similar(ele_1, ele_2):
    return SequenceMatcher(None, ele_1, ele_2).ratio()

class ScrapeFBAds:
    def __init__(self, exe_path, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("headless")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('w3c', False)
        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'ALL'}
        self.browser = webdriver.Chrome(desired_capabilities=caps,executable_path=exe_path, options=options) 
    
    def access_data(self, 
                    keyword="", 
                    active_status='all',
                    ad_type='political_and_issue_ads',
                    country='ALL'):
        query = {
            'active_status': active_status,
            'ad_type': ad_type,
            'country': country,
            'q': keyword
        }
        self.browser.get(
            "https://www.facebook.com/ads/library/?{}".format(urlencode(query))
        )
        time.sleep(3)
    
    def scroll_to_end(self, timeout=3):
      lenOfPage = self.browser.execute_script(
          "window.scrollTo(0, document.body.scrollHeight);\
           lenOfPage=document.body.scrollHeight;\
           return lenOfPage;"
      )
      match=False
      while(match==False):
          lastCount = lenOfPage
          time.sleep(timeout)
          lenOfPage = self.browser.execute_script(
              "window.scrollTo(0, document.body.scrollHeight);\
               var lenOfPage=document.body.scrollHeight;\
               return lenOfPage;"
          )
          if lastCount==lenOfPage:
              match=True
  
    def get_performance(self, url_image): 
        data = DataTrain.objects.filter(url_image=url_image).first()
        if data:
            print(data.title)
            try:
                jar = requests.cookies.RequestsCookieJar()
                for cookie in self.browser.get_cookies():
                    jar.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])
                ads_performance_logs = []
                for entry in self.browser.get_log('performance'):
                    msg = json.loads(entry['message'])
                    if msg.get('message', {}).get('method', {}) == 'Network.requestWillBeSent':
                        url = msg['message']['params']['request']['url']
                        if url.startswith('https://www.facebook.com/ads/library/async/insights/'):
                            ads_performance_logs.append(msg)
                for count, msg in enumerate(ads_performance_logs):
                    r = requests.post(msg['message']['params']['request']['url'],
                                        headers=msg['message']['params']['request']['headers'],
                                        data=msg['message']['params']['request']['postData'],
                                        cookies=jar)
                    r.raise_for_status()
                # print(data.title)
                # payload = 
                
                data.age_data = json.dumps(json.loads(r.text[9:])['payload']['ageGenderData'])
                data.view = json.loads(r.text[9:])['payload']['impressions']
                data.price = json.loads(r.text[9:])['payload']['spend']
                data.currency = json.loads(r.text[9:])['payload']['currency']
                # print(json.loads(r.text[1:]))
                # print("-------------------------------")
                # # print(json.loads(r.text[2:]))
                # print("-------------------------------")
                # # print(json.loads(r.text[3:]))
                # print("-------------------------------")
                # # print(json.loads(r.text[4:]))
                # print("-------------------------------")
                # # print(json.loads(r.text[5:]))
                # print("-------------------------------")
                # # print(json.loads(r.text[6:]))
                # print("-------------------------------")
                # # print(json.loads(r.text[7:]))
                # print("-------------------------------") 
                # print("-------------------------------")
                # print(json.loads(r.text[9:]))
                # print("-------------------------------")
                # print(json.loads(r.text[10:]))
                print('train-data-successful')
                data.save() 
            except:
                pass
            # for ad_log in payload['payload']['ageGenderData']:
            #     print(ad_log)
            # for ad_log in payload['payload']['impressions']:
            #     print(ad_log)
            # for ad_log in payload['payload']['locationData']:
            #     print(ad_log['reach'],ad_log['region'])
 
    def getHiddenInfor(self,length):
        try:
            for i in range(length):
                try:
                    print('ITEM',i)
                    self.browser.find_element_by_class_name('_7kfh').click()
                except ElementClickInterceptedException :
                    pass
                time.sleep(1)
                url_image = self.browser.find_element_by_class_name('_7jys').get_attribute('src')
                if url_image is None:
                    print('Don \'t search image url')
                    continue 
                self.get_performance(url_image) 
                webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                time.sleep(1)
                element = self.browser.find_element_by_class_name('_7owt') 
              
                self.browser.execute_script("""
                var element = arguments[0];
                element.parentNode.removeChild(element);
                """,element)
        except NoSuchElementException:
            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()

    def get_source(self):
      return self.browser.page_source
    
    def stop_scrape(self):
      self.browser.close()

def get_data_from_fb(keyword): 
    s = ScrapeFBAds("searchai/dataset/chromedriver")
    s.access_data(keyword=keyword, active_status='active')
    s.scroll_to_end(4)
    # s.getHiddenInfor(2)
    soup = BeautifulSoup(s.get_source(), "lxml")
    # all_ads = soup.find_all('div', class_="_7jyg _7jyh")

    all_ads = soup.find_all('div', class_="_7jvw _7jjw")
    
    

    for ad in all_ads:   
        ad_posted = ad.find('div', class_="_7jwu").get_text()
        ad_kind = ad.find('div', class_="_4ik4 _4ik5").get_text()
        ad_author = ad.find('div', class_="_7pg6 _3qn7 _61-3 _2fyi _3qng").get_text()
        ad_image_author = ad.find(['img'], class_=["_7pg4 img"])
        ad_description = ad.find('div', class_="_7jyr").get_text()
        ad_image = ad.find(['img'], class_=["_7jys img", "_7jys _7jyt img"])
        ad_info = ad.find_all('div', class_="_4ik4 _4ik5")
        ad_like = 'like'
        ad_title = 'title'
        ad_url_page = 'url_page'
        ad_brand = 'company' 

        for item in ad_info: 
            if len(item.find_all('a'))>0:
                ad_url_page = item.find_all('a')[0].get_text()  
            if(ad_info.index(item) == 3):
                ad_title = item.get_text()
            if(ad_info.index(item) == 4):
                ad_brand = item.get_text()
            if(ad_info.index(item) == 5):
                ad_like = item.get_text()
            if(ad_info.index(item) == 6): 
                ad_url_page = item.get_text()   

        #check data already exists
        if ad_image is None or ad_image_author is None or ad_image["src"] is None or ad_image_author["src"] is None:
            continue
     
        # hashed_id = str(ad_image["src"]).encode(encoding = 'UTF-8',errors = 'strict')
        data = DataTrain.objects.filter(author=ad_author).all() 
        flags = False
        for ele in data: 
            print(str(jellyfish.jaro_distance(ele.url_image, ad_image["src"])) + '/n')
            if jellyfish.jaro_distance(ele.url_image, ad_image["src"]) > 0.6: 
                if not keyword in ele.tags:  
                    ele.tags.append(keyword)
                    ele.save()
                flags = True
                print("No add")
                break
        if flags: 
            continue
        # image_file = save_picture_data(ad_image["src"])  
        image_author = ad_image_author["src"]
        
        data = DataTrain(   author=ad_author,
                            image_author=image_author,
                            title=ad_title,
                            description=ad_description,
                            # image_file=image_file,
                            url_page=ad_url_page,
                            like=ad_like,
                            brand=ad_brand,
                            date_posted=ad_posted,
                            kind=ad_kind,
                            url_image=ad_image["src"],
                            tags=[keyword]
                            )
        data.save()   
    
    print('count add times : ',len(all_ads))
    s.getHiddenInfor(len(all_ads)+1)
