import time

from searchai.models import DMMAdTrain

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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
            "https://dmmspy.com/spyads/dynamic-grid"
        )
        self.browser.find_element_by_class_name("fa-google").click()
        self.browser.find_element_by_class_name("zHQkBf").send_keys(username_gmail)
        webdriver.ActionChains(self.browser).send_keys(Keys.ENTER).perform()
        time.sleep(3)
        self.browser.find_element_by_class_name("zHQkBf").send_keys(password_gmail)
        webdriver.ActionChains(self.browser).send_keys(Keys.ENTER).perform()

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
                
    def get_source(self):
        return self.browser.page_source

    def stop_scrape(self):
        self.browser.close()

    def DMMSPYget(self): 
        countAdSuccess = 0
        while(True):
            try:
                element=self.browser.find_element_by_class_name('spy3-grid-container')
                page_name=self.browser.find_element_by_xpath('//*[@id="search-result-list"]/div/div[1]/div/div[3]/div/div/span/a[1]').text
                number_of_like =self.browser.find_element_by_class_name('label-primary').text
                number_of_comment=self.browser.find_element_by_class_name('label-info').text
                number_of_share=self.browser.find_element_by_class_name('label-success').text
                image_product=self.browser.find_element_by_xpath('//*[@id="search-result-list"]/div/div[1]/div/div[3]/a/img').get_attribute('src')
                detail_product_in_website= self.browser.find_element_by_class_name('linked-link').text
                time.sleep(1)

                if handleDMMAdTrain(page_name,number_of_like,number_of_comment,number_of_share,image_product,detail_product_in_website):
                    countAdSuccess += 1
                    
                self.browser.execute_script("""
                    var element = arguments[0];
                    element.parentNode.removeChild(element);
                    """,element)
            except NoSuchElementException:
                self.scroll_to_end(0.5)
            except NoSuchWindowException: 
                print('Ads Success',str(countAdSuccess))  
                pass

def handleDMMAdTrain(page_name,number_of_like,number_of_comment,number_of_share,image_product,detail_product_in_website):
    try:
        dmm_ad = DMMAdTrain(page_name=page_name,number_of_like=number_of_like,number_of_comment=number_of_comment,number_of_share=number_of_share,original_image_url=image_product,link_url=detail_product_in_website)
        dmm_ad.save()
        return True
    except:
        return False