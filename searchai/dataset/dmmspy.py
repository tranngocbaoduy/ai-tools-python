import time

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
            if count == 10 or lenOfPage > 10000: 
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


    def DMMSPYget(self): 
        # query = {
        #     'sort':'trending'
        # }
        # print(query)
        # self.browser.get(
        #     "https://dmmspy.com/spyads/dynamic-grid?sort=trending"
        # )
        countAdSuccess = 0
        while(True):
            try:
                
                element=self.browser.find_element_by_class_name('spy3-grid-container')
                
                page_name=self.browser.find_element_by_xpath('//*[@id="search-result-list"]/div/div[1]/div/div[3]/div/div/span/a[1]').text
                number_of_like =self.browser.find_element_by_class_name('label-primary').text
                number_of_comment=self.browser.find_element_by_class_name('label-info').text
                number_of_share=self.browser.find_element_by_class_name('label-success').text
                image_url=self.browser.find_element_by_xpath('//*[@id="search-result-list"]/div/div[1]/div/div[3]/a/img').get_attribute('src')
                image_url_profile =self.browser.find_element_by_xpath('//*[@id="search-result-list"]/div/div[1]/div/div[4]/div[1]/div[5]/a/img').get_attribute('src')

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
                #exit
                time.sleep(1)

                list_info = self.browser.find_elements_by_class_name("poi-modal")
                # for item in list_info:

                # for item in list_info:
                #     print(item.text)
                #     for i in item:
                #         print(i.text) 
                # print(list_info.get_attribute('div').get_attribute('div'))
                # print(list_info.get_attribute('div').get_attribute('div').get_attribute('div'))  
                # print(list_info.get_attribute('div').get_attribute('div').get_attribute('div')[0])  
                # print(list_info)
                post_id=self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[1]/a[1]').text
                page_id = self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[1]/a[2]').text
                platform = self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[1]/span[1]').text 
                image_url_mockup =self.browser.find_element_by_xpath('//*[@id="poi-mockup"]/a/img').get_attribute('src')

                self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[2]/div/div[1]/ul/li[2]/a').click()
                time.sleep(1)
                image_url_product=self.browser.find_element_by_xpath('//*[@id="poi-image"]/a/img').get_attribute('src')

                self.browser.find_element_by_xpath('//*[@id="modal-xl"]/div/div/div[2]/div/div[1]/ul/li[3]/a').click()
                time.sleep(0.3)
                
                description=self.browser.find_element_by_class_name('description').text  
                webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                
                #hết new
                print('Ads Success',str(countAdSuccess))
                if handleDMMAdTrain(post_id,
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
                                    platform):
                    countAdSuccess += 1
                self.browser.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                    """,element)
            except NoSuchElementException:
                print('NoSuchElementException',str(countAdSuccess))
                pass
            except NoSuchWindowException:
                print('NoSuchWindowException',str(countAdSuccess))
                pass
            except ElementNotVisibleException:
                print('ElementNotVisibleException',str(countAdSuccess))
                pass

def handleDMMAdTrain(post_id,
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
                    platform):
    if DMMAdTrain.objects.filter(post_id=post_id).first() is None:
        dmm_ad = DMMAdTrain( 
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
                            page_id=page_id)
        dmm_ad.save()
        
        return True
    else:
        print('Add Failed')
        return False