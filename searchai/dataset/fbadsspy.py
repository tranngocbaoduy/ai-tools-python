# lib to run selenium and analytic data
import os
import time
import json
import lxml
import requests 

from searchai.models import DataTrain, AdditionalInfo, InfoAd, FBAdTrain

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, ElementClickInterceptedException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 

#libs compare two string
from difflib import SequenceMatcher
import jellyfish

from urllib.parse import urlencode 
import urllib.parse as urlparse

class ScrapeFBAds:
    def __init__(self, exe_path, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("headless")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        # options.add_argument('--proxy-server=195.171.16.146:8080')
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('w3c', False)
        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'ALL'}
        self.browser = webdriver.Chrome(desired_capabilities=caps,executable_path=exe_path, options=options) 
    
    def access_data(self, 
                    keyword="",  
                    view_all_page_id="",
                    active_status='active',
                    ad_type='all',
                    impression_search_field='has_impressions_lifetime',
                    country='ALL'
                    ):
        query = {
            'active_status': active_status,
            'ad_type': ad_type,
            'country': country,
            'impression_search_field':impression_search_field, 
            'q': keyword,
            'view_all_page_id': view_all_page_id
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
        count = 0
        while(True):
            lastCount = lenOfPage 
            time.sleep(timeout)
            lenOfPage = self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);\
                var lenOfPage=document.body.scrollHeight;\
                return lenOfPage;"
            )
            if lastCount==lenOfPage: 
                count += 1
            if count == 10:
                return False
        return True 

    def searchAds(self, tags):
        print('        |----------------   search FB ads   ------------------|   ')     
        print('') 
        i = 0
        countAds = 0
        countAdSuccess = 0
        countAdConflictOrFailed = 0
        if self.scroll_to_end(1) == False:
            print('                          YOU REACH BOTTOM') 
        try:
            jar = requests.cookies.RequestsCookieJar()
            for cookie in self.browser.get_cookies():
                jar.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])
            ads_performance_logs = []
            for entry in self.browser.get_log('performance'):
                msg = json.loads(entry['message'])
                if msg.get('message', {}).get('method', {}) == 'Network.requestWillBeSent':
                    url = msg['message']['params']['request']['url']
                    if url.startswith('https://www.facebook.com/ads/library/async/search_ads/'):
                        ads_performance_logs.append(msg)
            for count, msg in enumerate(ads_performance_logs):
                r = requests.post(msg['message']['params']['request']['url'],
                                    headers=msg['message']['params']['request']['headers'],
                                    data=msg['message']['params']['request']['postData'],
                                    cookies=jar)
                r.raise_for_status() 
                ans = json.loads(r.text[9:])['payload']['results']
                for item in ans: 
                    countAds += len(item) 
                    if FBAdTrain.objects.filter(ad_id=item[0]['adid']).first() is None:
                        # handele infomation to add ads to db
                        additional_info = handleAdditionalInfo(item[0])   
                        snap_shot = handleInfoAd(item[0], additional_info)
                        handleFBAdTrain(item[0], snap_shot, tags)
                        countAdSuccess += 1 
                    else:
                        countAdConflictOrFailed +=1 
                    print('Item - step 1', i)
                    i+=1
        except NoSuchWindowException:
            pass      
        print('')
        print('        |-----------------------------------------------------|   ')     
        print('                       Ads ',str(countAds))  
        print('                       Ads Success',str(countAdSuccess))  
        print('                       Ads Failed Or Conflict',str(countAdConflictOrFailed))   
        self.getHiddenInfor() 
 
    def getHiddenInfor(self): 
        i =0 
        list = self.browser.find_elements_by_class_name('_7kfh') 
        for item in list: 
            print('Item - step 2', i)
            i+=1 
            self.browser.execute_script("arguments[0].click();", item) 
            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
            time.sleep(2) 
        # list_old_version = self.browser.find_elements_by_class_name('_7tv4')
        # i =0 
        # for item in list_old_version:
        #     print('Item', i)
        #     i+=1 
        #     self.browser.execute_script("arguments[0].click();", item)
        #     time.sleep(1) 
        time.sleep(3) 
        
        self.get_archive_info() 

    def get_archive_info(self):    
        i = 0
        countAdInfoSuccess = 0
        countAdInfoFailed = 0  
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
        for count, msg in enumerate(ads_performance_logs[-1]):
            r = requests.post(msg['message']['params']['request']['url'],
                                headers=msg['message']['params']['request']['headers'],
                                data=msg['message']['params']['request']['postData'],
                                cookies=jar)           
            time.sleep(1)          
            r.raise_for_status()  
            #parsed get ad archive id
            parsed = urlparse.urlparse(str(msg['message']['params']['request']['url'])) 
            ad_archive_id = urlparse.parse_qs(parsed.query)['ad_archive_id'][0]
            if ad_archive_id is not None: 
                payload = json.loads(r.text[9:])['payload']
                ad = FBAdTrain.objects.filter(ad_archive_id=ad_archive_id).first() 
                if ad is not None:
                    try:
                        if payload['ageGenderData'] is not None:
                            ad.age_data= json.dumps(payload['ageGenderData'])
                        if payload['impressions'] is not None:
                            ad.view = payload['impressions']
                        if payload['spend'] is not None:
                            ad.price = payload['spend']
                        if payload['currency'] is not None:
                            ad.currency = payload['currency']  
                        if payload['locationData'] is not None:
                            ad.region_data= json.dumps(payload['locationData']) 
                    except:
                        ad.save()
                        pass
                    ad.save() 
                    countAdInfoSuccess += 1
                else:
                    countAdInfoFailed += 1
            else:
                countAdInfoFailed += 1
            print('Item - step 3', i)
            i+=1
        
        print('                       Ads Info Success Or Update',str(countAdInfoSuccess))  
        print('                       Ads Info Failed',str(countAdInfoFailed))  
        print('        |-----------------------------------------------------|   ')
        print('')

    def get_source(self):
      return self.browser.page_source
    
    def stop_scrape(self):
      self.browser.close()

def handleAdditionalInfo(element): 
    # create AdditionalInfo
    city = 'city'
    committee_id = 'committee_id' 
    director_name = 'director_name'
    email = 'email'
    phone_number = 'phone_number'
    point_of_contact = 'point_of_contact'
    state = 'state'
    street_address_1 = 'street_address_1'
    street_address_2 = 'street_address_2'
    website = 'website'
    treasurer_name = 'treasurer_name'
    zipcode = 'zipcode' 

    dummy_additional_info = element['snapshot']['additional_info']
    if dummy_additional_info is not None:   
         
        if dummy_additional_info['city'] is not None:
            city = dummy_additional_info['city'] 
        if dummy_additional_info['committee_id'] is not None:
            committee_id = dummy_additional_info['committee_id'] 
        if dummy_additional_info['director_name'] is not None:
            director_name = dummy_additional_info['director_name']
        if dummy_additional_info['email'] is not None:
            email = dummy_additional_info['email']
        if dummy_additional_info['phone_number'] is not None:
            phone_number = dummy_additional_info['phone_number']
        if dummy_additional_info['point_of_contact'] is not None:
            point_of_contact = dummy_additional_info['point_of_contact']
        if dummy_additional_info['state'] is not None:    
            state = dummy_additional_info['state']
        if dummy_additional_info['street_address_1'] is not None:
            street_address_1 = dummy_additional_info['street_address_1']
        if dummy_additional_info['street_address_2'] is not None:    
            street_address_2 = dummy_additional_info['street_address_2']
        if dummy_additional_info['treasurer_name'] is not None:
            treasurer_name = dummy_additional_info['treasurer_name']
        if dummy_additional_info['website'] is not None:
            website = dummy_additional_info['website']
        if dummy_additional_info['zipcode'] is not None:
            zipcode = dummy_additional_info['zipcode'] 

    # additional_info = AdditionalInfo(city=city,committee_id=committee_id,director_name=director_name,email=email,phone_number=phone_number,point_of_contact=point_of_contact,state=state,street_address_1=street_address_1,street_address_2=street_address_2,treasurer_name=treasurer_name,website=website,zipcode=zipcode) 
    additional_info = AdditionalInfo(city=city,committee_id=committee_id,director_name=director_name,email=email,phone_number=phone_number,point_of_contact=point_of_contact,state=state,street_address_1=street_address_1,street_address_2=street_address_2,treasurer_name=treasurer_name,website=website,zipcode=zipcode) 
    return additional_info.to_json()  
    
def handleInfoAd(element, additional_info): 
    ad_creative_id = 'ad_creative_id'
    additional_info = additional_info
    by_line = 'by_line'
    caption = 'caption'
    country_iso_code = 'country_iso_code'
    creation_time = 'creation_time'
    current_page_name = 'current_page_name'
    original_image_url = 'original_image_url'
    resize_image_url = 'resize_image_url'
    instagram_actor_name = 'instagram_actor_name'
    instagram_profile_pic_url = 'instagram_profile_pic_url'
    link_description = 'link_description'
    link_url = 'link_url'
    page_categories = 'page_categories'
    page_id = 'page_id'
    page_is_deleted = 'page_is_deleted'
    page_like_count = 'page_like_count'
    page_name = 'page_name'
    page_profile_picture_url = 'page_profile_picture_url'
    page_profile_uri = 'page_profile_uri'
    page_welcome_message = 'page_welcome_message'
    root_reshared_post = 'root_reshared_post'
    title = 'title'
    version = 'version'
        
    dummy_snap_shot = element['snapshot']
 
    if dummy_snap_shot is not None: 
        if dummy_snap_shot['ad_creative_id'] is not None:
            ad_creative_id = str(dummy_snap_shot['ad_creative_id'])
        if dummy_snap_shot['additional_info'] is not None:
            additional_info = additional_info
        if dummy_snap_shot['byline'] is not None:
            by_line = dummy_snap_shot['byline']
        if dummy_snap_shot['caption'] is not None:
            caption = dummy_snap_shot['caption']
        if dummy_snap_shot['country_iso_code'] is not None:
            country_iso_code = dummy_snap_shot['country_iso_code']
        if dummy_snap_shot['creation_time'] is not None:
            creation_time = dummy_snap_shot['creation_time']
        if dummy_snap_shot['current_page_name'] is not None:
            current_page_name = dummy_snap_shot['current_page_name']
        if dummy_snap_shot['images'] is not None and len(dummy_snap_shot['images']) > 0:   
            if dummy_snap_shot['images'][0]['original_image_url'] is not None:
                original_image_url = dummy_snap_shot['images'][0]['original_image_url']
            if dummy_snap_shot['images'][0]['resized_image_url'] is not None:
                resize_image_url = dummy_snap_shot['images'][0]['resized_image_url'] 
        if dummy_snap_shot['instagram_actor_name'] is not None:
            instagram_actor_name = dummy_snap_shot['instagram_actor_name']
        if dummy_snap_shot['instagram_profile_pic_url'] is not None:
            instagram_profile_pic_url = dummy_snap_shot['instagram_profile_pic_url']
        if dummy_snap_shot['link_description'] is not None:
            link_description = dummy_snap_shot['link_description']
        if dummy_snap_shot['link_url'] is not None:
            link_url = dummy_snap_shot['link_url']
        if dummy_snap_shot['page_categories'] is not None:
            page_categories = str(dummy_snap_shot['page_categories'])
        if dummy_snap_shot['page_id'] is not None:
            page_id = str(dummy_snap_shot['page_id'])
        if dummy_snap_shot['page_is_deleted'] is not None:
            page_is_deleted = dummy_snap_shot['page_is_deleted']
        if dummy_snap_shot['page_like_count'] is not None:
            page_like_count = str(dummy_snap_shot['page_like_count'])
        if dummy_snap_shot['page_name'] is not None:
            page_name = dummy_snap_shot['page_name']
        if dummy_snap_shot['page_profile_picture_url'] is not None:
            page_profile_picture_url = dummy_snap_shot['page_profile_picture_url']
        if dummy_snap_shot['page_profile_uri'] is not None:
            page_profile_uri = dummy_snap_shot['page_profile_uri']
        if dummy_snap_shot['page_welcome_message'] is not None:
            page_welcome_message = dummy_snap_shot['page_welcome_message']
        if dummy_snap_shot['root_reshared_post'] is not None:
            root_reshared_post = dummy_snap_shot['root_reshared_post']
        if dummy_snap_shot['title'] is not None:
            title = dummy_snap_shot['title']
        if dummy_snap_shot['version'] is not None:
            version = str(dummy_snap_shot['version'])

    snap_shot = InfoAd(
        ad_creative_id=ad_creative_id,additional_info=additional_info,by_line=by_line,caption=caption,country_iso_code=country_iso_code,creation_time=creation_time,
        current_page_name=current_page_name,original_image_url=original_image_url,resize_image_url=resize_image_url,instagram_actor_name=instagram_actor_name,instagram_profile_pic_url=instagram_profile_pic_url,
        link_description=link_description,link_url=link_url,page_categories=page_categories,page_id=page_id,page_is_deleted=page_is_deleted,page_like_count=page_like_count,
        page_name=page_name,page_profile_picture_url=page_profile_picture_url,page_profile_uri=page_profile_uri,page_welcome_message=page_welcome_message,root_reshared_post=root_reshared_post,
        title=title,version=version)
    return snap_shot.to_json() 

def handleFBAdTrain(element, snap_shot, tag):  
    ad_id = 'ad_id'
    ad_archive_id = 'ad_archive_id'
    end_date= 0
    start_date = 0
    gated_type = 'gated_type'
    is_active = False
    is_profile_page = False
    is_promoted_news= False
    page_id = 'page_id'
    page_name = 'page_name'
    snap_shot = snap_shot
    tags = [tag]
 
    if element['adid'] is not None:
        ad_id = element['adid'] 
    if element['adArchiveID'] is not None:
        ad_archive_id = element['adArchiveID']
    if element['endDate'] is not None:
        end_date= element['endDate']
    if element['startDate'] is not None:
        start_date = element['startDate']
    if element['gatedType'] is not None:
        gated_type = element['gatedType']
    if element['isActive'] is not None:    
        is_active = element['isActive']
    if element['isProfilePage'] is not None:
        is_profile_page = element['isProfilePage']
    if element['isPromotedNews'] is not None:
        is_promoted_news= element['isPromotedNews']
    if element['pageID'] is not None:
        page_id = element['pageID']
    if element['pageName'] is not None:
        page_name = element['pageName']
 
    adTrain = FBAdTrain(ad_id=ad_id,ad_archive_id=ad_archive_id,end_date=end_date,start_date=start_date,gated_type=gated_type,is_active=is_active,is_profile_page=is_profile_page,
                    is_promoted_news=is_promoted_news,page_id=page_id,page_name=page_name,snap_shot=snap_shot,tags=tags)
    adTrain.save()


# def get_data_from_fb(keyword): 
#     s = ScrapeFBAds("searchai/dataset/chromedriver")
#     s.access_data(keyword=keyword, active_status='active')
#     s.scroll_to_end(3)
#     s.searchAds()
    # s.getPageId()
    
    # s.getHiddenInfor(2)
    # soup = BeautifulSoup(s.get_source(), "lxml")
    # # all_ads = soup.find_all('div', class_="_7jyg _7jyh")

    # all_ads = soup.find_all('div', class_="_7jvw _7jjw")
    
    

    # for ad in all_ads:   
    #     ad_posted = ad.find('div', class_="_7jwu").get_text()
    #     ad_kind = ad.find('div', class_="_4ik4 _4ik5").get_text()
    #     ad_author = ad.find('div', class_="_7pg6 _3qn7 _61-3 _2fyi _3qng").get_text()
    #     ad_image_author = ad.find(['img'], class_=["_7pg4 img"])
    #     ad_description = ad.find('div', class_="_7jyr").get_text()
    #     ad_image = ad.find(['img'], class_=["_7jys img", "_7jys _7jyt img"])
    #     ad_info = ad.find_all('div', class_="_4ik4 _4ik5")
    #     ad_like = 'like'
    #     ad_title = 'title'
    #     ad_url_page = 'url_page'
    #     ad_brand = 'company' 

    #     for item in ad_info: 
    #         if len(item.find_all('a'))>0:
    #             ad_url_page = item.find_all('a')[0].get_text()  
    #         if(ad_info.index(item) == 3):
    #             ad_title = item.get_text()
    #         if(ad_info.index(item) == 4):
    #             ad_brand = item.get_text()
    #         if(ad_info.index(item) == 5):
    #             ad_like = item.get_text()
    #         if(ad_info.index(item) == 6): 
    #             ad_url_page = item.get_text()   

    #     #check data already exists
    #     if ad_image is None or ad_image_author is None or ad_image["src"] is None or ad_image_author["src"] is None:
    #         continue
     
    #     # hashed_id = str(ad_image["src"]).encode(encoding = 'UTF-8',errors = 'strict')
    #     data = DataTrain.objects.filter(author=ad_author).all() 
    #     flags = False
    #     for ele in data: 
    #         print(str(jellyfish.jaro_distance(ele.url_image, ad_image["src"])) + '/n')
    #         if jellyfish.jaro_distance(ele.url_image, ad_image["src"]) > 0.6: 
    #             if not keyword in ele.tags:  
    #                 ele.tags.append(keyword)
    #                 ele.save()
    #             flags = True
    #             print("No add")
    #             break
    #     if flags: 
    #         continue
    #     # image_file = save_picture_data(ad_image["src"])  
    #     image_author = ad_image_author["src"]
        
    #     data = DataTrain(   author=ad_author,
    #                         image_author=image_author,
    #                         title=ad_title,
    #                         description=ad_description,
    #                         # image_file=image_file,
    #                         url_page=ad_url_page,
    #                         like=ad_like,
    #                         brand=ad_brand,
    #                         date_posted=ad_posted,
    #                         kind=ad_kind,
    #                         url_image=ad_image["src"],
    #                         tags=[keyword]
    #                         )
    #     data.save()   
    
    # print('count add times : ',len(all_ads))
    
    # s.getHiddenInfor(len(all_ads)+1)


    # def getPageId(self):
    #     print('Get PageId')
    #     try:
    #         jar = requests.cookies.RequestsCookieJar()
    #         for cookie in self.browser.get_cookies():
    #             jar.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])
    #         ads_performance_logs = []
    #         for entry in self.browser.get_log('performance'):
    #             msg = json.loads(entry['message'])
    #             if msg.get('message', {}).get('method', {}) == 'Network.requestWillBeSent':
    #                 url = msg['message']['params']['request']['url']
    #                 if url.startswith('https://www.facebook.com/ads/library/async/search_filters/'):
    #                     ads_performance_logs.append(msg)
    #         for count, msg in enumerate(ads_performance_logs):
    #             r = requests.post(msg['message']['params']['request']['url'],
    #                                 headers=msg['message']['params']['request']['headers'],
    #                                 data=msg['message']['params']['request']['postData'],
    #                                 cookies=jar)
    #             r.raise_for_status()
            # print(data.title)
            # payload = 
            # ans = json.loads(r.text[9:])

            # listInfo = ans['payload']['1']   
            # listPageId = list(ans['payload']['1']) 
            # print('-----')
            # for item in listPageId:
            #     print(item)
            #     print(listInfo[item])
            #     print('----------') 
        # except:
        #     pass
