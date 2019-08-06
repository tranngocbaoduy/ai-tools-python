import os
import secrets

from PIL import Image
 
# import the necessary packages
# from skimage.measure import structural_similarity as ssim
# import matplotlib.pyplot as plt
# import numpy as np
# import cv2

from flask import current_app  
from io import BytesIO 
from datetime import datetime

from searchai.models import DataTrain, AdditionalInfo, InfoAd, FBAdTrain, DMMAdTrain, AdTrain
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

def get_data_from_fb(id,keyword): 
    s = ScrapeFBAds("searchai/dataset/chromedriver")
    s.access_data(view_all_page_id=id,keyword=keyword, active_status='active')
    s.searchAds(keyword)

def get_data_from_dmmspy(): 
    dmm_spy_ads = ScrapeDMMSPYAds("searchai/dataset/chromedriver")
    dmm_spy_ads.access_data("baoduy19971997@gmail.com","mushroomzz99")
    # dmm_spy_ads.scroll_to_end(0.5)
    dmm_spy_ads.DMMSPYget()


# def mse(imageA, imageB):
# 	# the 'Mean Squared Error' between the two images is the
# 	# sum of the squared difference between the two images;
# 	# NOTE: the two images must have the same dimension
# 	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
# 	err /= float(imageA.shape[0] * imageA.shape[1])
	
# 	# return the MSE, the lower the error, the more "similar"
# 	# the two images are
# 	return err
 
# def compare_images(imageA, imageB, title):
# 	# compute the mean squared error and structural similarity
# 	# index for the images
# 	m = mse(imageA, imageB)
# 	s = ssim(imageA, imageB)
 
# 	# setup the figure
# 	fig = plt.figure(title)
# 	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
 
# 	# show first image
# 	ax = fig.add_subplot(1, 2, 1)
# 	plt.imshow(imageA, cmap = plt.cm.gray)
# 	plt.axis("off")
 
# 	# show the second image
# 	ax = fig.add_subplot(1, 2, 2)
# 	plt.imshow(imageB, cmap = plt.cm.gray)
# 	plt.axis("off")
 
# 	# show the images
# 	plt.show()
 
# def check_image_similar():
#     imageA= Image.open("searchai/static/train_pics/avatar.png")
#     imageB= Image.open("searchai/static/train_pics/avatar.1.png")
#     mse(imageA, imageB)


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

def convertToMyAd():
    countDMM = 0
    listDMM = DMMAdTrain.objects.all()
    
    for item in listDMM:  
        if AdTrain.objects.filter(post_id=item.post_id).first() is None and item.is_active:
            myAd = AdTrain( page_id=item.page_id,
                            page_name=item.page_name,
                            post_id=item.post_id,
                            number_of_like=item.number_of_like,
                            number_of_comment=item.number_of_comment,
                            number_of_share=item.number_of_share, 
                            image_url_mockup=item.image_url_mockup,
                            image_url_product=item.image_url_product,
                            image_url_profile=item.image_url_profile,
                            link_url=item.link_url,
                            description=item.description,
                            platform=item.platform)
            myAd.save()
            countDMM +=1
    print('        |------------------   convert ads   ------------------|   ')     
    print('                         DMM Ads: ',str(countDMM))  

    countFB = 0

    listFB = FBAdTrain.objects.all()
    for item in listFB: 
        if AdTrain.objects.filter(page_id=item.page_id).filter(ad_id=item.ad_id).first() is None and item.is_active:
            item['snap_shot'] = json.loads(item['snap_shot']) 
            item['snap_shot']['additional_info'] = json.loads(item['snap_shot']['additional_info'])  
            myAd = AdTrain( page_id=item.page_id,
                            page_name=item.page_name,
                            ad_id=item.ad_id, 

                            title=item.snap_shot['title'], 
                            image_url_mockup=item.snap_shot['original_image_url'],
                            image_url_product=item.snap_shot['original_image_url'],
                            image_url_profile=item.snap_shot['page_profile_picture_url'],
                            link_url=item.snap_shot['link_url'],
                            description=item.snap_shot['link_description'], 
                            
                            start_date=item.start_date,
                            tags=item.tags,
                            age_data=item.age_data,
                            view=item.view,
                            currency=item.currency,
                            price=item.price,
                            region_data=item.region_data)
            myAd.save()
            countFB +=1
    print('                         FB Ads: ',str(countFB)) 
    print('                         Total: ',str(countFB+countDMM)) 
    print('        |-----------------------------------------------------|   ')
    print('') 