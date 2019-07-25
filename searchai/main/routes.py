from flask import request, render_template, Blueprint, send_from_directory, current_app
# from searchai.main.utils import index_data, description_search
# from searchai.capgen import CaptionGenerator 
from searchai.models import Respone
from searchai.users.utils import verify_login
from flask_login import logout_user
import json 
import os 

# gencap = CaptionGenerator()

main = Blueprint('main', __name__)
  
# index_data()

@main.route('/', methods=['GET', 'POST'])
def index():
   return render_template('index.html')


@main.route('/favicon.ico', methods=['GET', 'POST'])
def favicon():
    return '../favicon.ico'

@main.route('/webhooks', methods=['GET', 'POST'])
def webhooks():
    a = {
        "entry": [
            {
            "time": 1520383571,
            "changes": [
                {
                "field": "photos",
                "value":
                    {
                    "verb": "update",
                    "object_id": "10211885744794461"
                    }
                }
            ],
            "id": "10210299214172187",
            "uid": "10210299214172187"
            }
        ],
        "object": "user"
    }
    return json.dumps(a)
# @main.route('/search', methods=['GET', 'POST'])
# def product():  
#     global gencap
#     if request.method == 'POST': 
#         query = request.get_json()['query'] 
#         results = description_search(query,20) 
#         payload = {
#             "products": json.dumps(results) 
#         } 
#         message = "GET PRODUCT SUCCESS"
#         answer = Respone(True, payload, message)   
#     else:
#         answer = Respone(False, {}, "GET PRODUCT FAILED")   
#     return json.dumps(answer)  

# @main.route('/get_products', methods=['GET', 'POST'])
# def get_products():  
#     global gencap 
#     try:
#         token = request.get_json()['token']  
#         if token and request.method == 'POST' and verify_login(token):   
#             results = description_search('a',200) 
#             payload = {
#                 "products": json.dumps(results) 
#             } 
#             message = "GET PRODUCTS SUCCESS" 
#             return json.dumps(Respone(True, payload, message))  
#         return json.dumps(Respone(False, {}, "Unauthorized"))  
#     except:
#         return json.dumps(Respone(False, {}, "Unauthorized"))    

# @main.route('/get_product', methods=['GET', 'POST'])
# def get_product():  
#     global gencap
#     if request.method == 'POST':  
#         result = description_search('a',1) 
#         payload = {
#             "product": json.dumps(result) 
#         } 
#         message = "GET PRODUCT SUCCESS"
#         answer = Respone(True, payload, message)   
#     else:
#         answer = Respone(False, {}, "GET PRODUCT FAILED")   
#     return json.dumps(answer)  

# # @main.route('/product', methods=['GET', 'POST'])
# # def product():  
# #     global gencap
# #     if request.method == 'POST':
# #         query = request.get_json()['query']
# #         answers = description_search(query)
# #         k = json.dumps(answers) 
# #         return k
# #     else:  
# #         return render_template('index.html')


# # @posts.route("/product/<product_id>")
# # def product(product_id):   
# #     global gencap
# #     if request.method == 'POST':
# #         query = request.get_json()['query']
# #         answers = description_search(query)
# #         k = json.dumps(answers) 
# #         return k
# #     else:  
# #         return render_template('index.html')