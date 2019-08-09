import time 
import json
import lxml
import requests 

from searchai.models import DMMAdTrain

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, ElementClickInterceptedException, ElementNotVisibleException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


from urllib.parse import urlencode 
import urllib.parse as urlparse

class ScrapeDMMSPYAds:
    def __init__(self, exe_path, headless=False):
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("headless")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('w3c', False)
        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'ALL'}
        self.browser = webdriver.Chrome(desired_capabilities=caps,executable_path=exe_path, options=options)
        self.browser.get(
            "https://dmmspy.com/"
        )

    def access_data(self,username_gmail,password_gmail):
        
        self.browser.get(
            "https://dmmspy.com/spyads/dynamic-grid?sort=trending"
        )
         
        # WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.find_element_by_class_name, 'fa-google')))
        time.sleep(8)
        self.browser.find_element_by_class_name("fa-google").click()
        self.browser.find_element_by_class_name("zHQkBf").send_keys(username_gmail)
        webdriver.ActionChains(self.browser).send_keys(Keys.ENTER).perform()
        time.sleep(3)
        self.browser.find_element_by_class_name("zHQkBf").send_keys(password_gmail)
        webdriver.ActionChains(self.browser).send_keys(Keys.ENTER).perform()
        # time.sleep(3)
        

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
            if count == 10 or lenOfPage > 1000: 
                break;
 
    def get_source(self):
        return self.browser.page_source

    def stop_scrape(self):
        self.browser.close()

    # def DMMSPYget(self): 
    #     countAdSuccess = 0
    #     while(True):
    #         try:
    #             element=self.browser.find_element_by_class_name('spy3-grid-container')
    #             page_name=self.browser.find_element_by_xpath('//*[@id="search-result-list"]/div/div[1]/div/div[3]/div/div/span/a[1]').text
    #             number_of_like =self.browser.find_element_by_class_name('label-primary').text
    #             number_of_comment=self.browser.find_element_by_class_name('label-info').text
    #             number_of_share=self.browser.find_element_by_class_name('label-success').text
    #             image_product=self.browser.find_element_by_xpath('//*[@id="search-result-list"]/div/div[1]/div/div[3]/a/img').get_attribute('src')
    #             detail_product_in_website= self.browser.find_element_by_class_name('linked-link').text
    #             time.sleep(1)

    #             if handleDMMAdTrain(page_name,number_of_like,number_of_comment,number_of_share,image_product,detail_product_in_website):
    #                 countAdSuccess += 1
                    
    #             self.browser.execute_script("""
    #                 var element = arguments[0];
    #                 element.parentNode.removeChild(element);
    #                 """,element)
    #         except NoSuchElementException:
    #             self.scroll_to_end(0.5)
    #         except NoSuchWindowException: 
    #             print('Ads Success',str(countAdSuccess))  
    #             pass
    # def DMMSPYget1(self):  
    #     countAdSuccess = 0
    #     countBug = 0
    #     # while(True):
    #     # if countBug == 40:
    #     #     break;
    #     try:  

    #         elements=self.browser.find_elements_by_class_name('spy3-grid')  
    #         count=0
    #         for item in elements:
    #             listInfo = item.text.split("\n")
    #             for i in listInfo:
    #                 print(i)
    #             count+=1
    #             print('------------------------------------------------')
    #         print("count=",count)   

    #     except NoSuchElementException: 
    #         print('NoSuchElementException',str(countAdSuccess))
    #         countBug+=1
    #         pass
    #     except NoSuchWindowException:
    #         print('NoSuchWindowException',str(countAdSuccess))
    #         countBug+=1
    #         pass
    #     except ElementNotVisibleException:
    #         print('ElementNotVisibleException',str(countAdSuccess))
    #         countBug+=1
    #         pass

    def DMMSPYget(self):  
        countAdSuccess = 0
        countBug = 0
        while(True):
            if countBug == 40:
                break;
            try: 
                element=self.browser.find_element_by_class_name('spy3-grid-container')  

                # for item in elements:
                #     print(item)
                #     print(item.text)

                page_name=self.browser.find_element_by_xpath('//*[@id="search-result-list"]/div/div[1]/div/div[3]/div/div/span/a[1]').text
                print("page_name")
                number_of_like =self.browser.find_element_by_class_name('label-primary').text
                print("number_of_like")
                number_of_comment=self.browser.find_element_by_class_name('label-info').text
                print("number_of_comment")
                number_of_share=self.browser.find_element_by_class_name('label-success').text
                print("number_of_share")
                image_url=self.browser.find_element_by_xpath('//*[@id="search-result-list"]/div/div[1]/div/div[3]/a/img').get_attribute('src')
                print("image_url")
                
                link_url= self.browser.find_element_by_class_name('linked-link').text
                
                time.sleep(3)
                #new
                #then click in image get post id page id
                try:
                    self.browser.find_element_by_class_name("center-block").click()
                except  ElementNotVisibleException:
                    pass
                except ElementClickInterceptedException:
                    pass
                print("click into image")    
                #exit
                time.sleep(1)

                list_info = self.browser.find_elements_by_class_name("poi-modal")
                # for item in list_info:
                jar = requests.cookies.RequestsCookieJar()
                for cookie in self.browser.get_cookies():
                    jar.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'])
                
                for entry in self.browser.get_log('performance'):
                    msg = json.loads(entry['message'])
                    if msg.get('message', {}).get('method', {}) == 'Network.requestWillBeSent':
                        url = msg['message']['params']['request']['url']
                        if url.startswith('https://dmmspy.com/spyads/post-info?'):  
                            #parsed get ad archive id
                            parsed = urlparse.urlparse(str(msg['message']['params']['request']['url'])) 
                            owner_id = urlparse.parse_qs(parsed.query)['owner_id'][0]
                            dmm_id = urlparse.parse_qs(parsed.query)['id'][0] 
                            break; 
                            
                time.sleep(3)
                post_id=self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[1]/a[1]').text
                print("post_id")
                page_id = self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[1]/a[2]').text
                print("page_id")
                platform = self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[1]/span[1]').text 
                print("flatform")
                self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[2]/div/div[1]/ul/li[1]/a').click()
                time.sleep(1) 
                image_url_mockup =self.browser.find_element_by_xpath('//*[@id="poi-mockup"]/a/img').get_attribute('src')
                print("image_url_mockup")
                self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[2]/div/div[1]/ul/li[2]/a').click()
                time.sleep(1)

                
                image_url_product=self.browser.find_element_by_xpath('//*[@id="poi-image"]/a/img').get_attribute('src')
                print("image_url_product")
                self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[2]/div/div[1]/ul/li[3]/a').click()
                time.sleep(1) 
                
                start_date = self.browser.find_element_by_xpath('//*[@id="poi-post-detail"]/div/div/div[2]').get_attribute('title')
                domain = self.browser.find_element_by_xpath('//*[@id="poi-post-detail"]/div/div/div[3]').text 
                product_url = self.browser.find_element_by_xpath('//*[@id="poi-post-detail"]/div/div/div[4]').text 
                pixel_id = self.browser.find_element_by_xpath('//*[@id="poi-post-detail"]/div/div/div[5]').text
                title = self.browser.find_element_by_xpath('//*[@id="poi-post-detail"]/div/div/div[6]').text
                
                

                try:
                    # image_url_profile =self.browser.find_element_by_xpath('//*[@id="poi-post-detail"]/div/div/div[1]/div[3]/a/img').get_attribute('src')
                    image_url_profile =self.browser.find_element_by_class_name('post-owner-avatar').get_attribute('src')
                except NoSuchElementException: 
                    image_url_profile=""
                    print('NoSuchElementException',"NO image_url_profile")
                    countBug+=1
                    pass 

                description=self.browser.find_element_by_class_name('description').text  
                print("description")
                webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                #hết new
                if handleDMMAdTrain(dmm_id,
                                    post_id,
                                    page_id,
                                    page_name,
                                    number_of_like,
                                    number_of_comment,
                                    number_of_share,
                                    image_url,
                                    image_url_mockup,
                                    image_url_product,
                                    image_url_profile,
                                    link_url,
                                    description,
                                    platform,
                                    start_date,
                                    domain,
                                    title,
                                    pixel_id,
                                    product_url):
                    countAdSuccess += 1
                self.browser.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                    """,element)
            except NoSuchElementException: 
                print('NoSuchElementException',str(countAdSuccess))
                countBug+=1
                pass
            except NoSuchWindowException:
                print('NoSuchWindowException',str(countAdSuccess))
                countBug+=1
                pass
            except ElementNotVisibleException:
                print('ElementNotVisibleException',str(countAdSuccess))
                countBug+=1
                pass
        
        print('Ads Success',str(countAdSuccess))

def handleDMMAdTrain(dmm_id,
                    post_id,
                    page_id,
                    page_name,
                    number_of_like,
                    number_of_comment,
                    number_of_share,
                    image_url,
                    image_url_mockup,
                    image_url_product,
                    image_url_profile,
                    link_url,
                    description,
                    platform,
                    start_date,
                    domain,
                    title,
                    pixel_id,
                    product_url):
    if DMMAdTrain.objects.filter(page_id=page_id).filter(post_id=post_id).first() is None:
        dmm_ad = DMMAdTrain( 
                            dmm_id=dmm_id,
                            page_name=page_name,
                            number_of_like=number_of_like,
                            number_of_comment=number_of_comment,
                            number_of_share=number_of_share,
                            image_url=image_url, 
                            image_url_mockup=image_url_mockup,
                            image_url_product=image_url_product,
                            image_url_profile=image_url_profile,
                            description=description,
                            link_url=link_url,
                            platform=platform,
                            post_id=post_id,
                            page_id=page_id,
                            start_date=start_date,
                            domain=domain,
                            title=title,
                            pixel_id=pixel_id,
                            product_url=product_url)
        dmm_ad.save()
        
        return True
    else:
        print('Add Failed')
        return False