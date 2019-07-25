from flask import request, render_template, Blueprint,abort
import json
from searchai.models import DataTrain, Respone
from searchai import db, bcrypt 
# from flask_login import login_user, current_user, logout_user, login_required
from searchai.dataset.utils import get_data_from_fb
from searchai.users.utils import verify_login 

dataset = Blueprint('dataset', __name__)

@dataset.route("/train_data", methods=['GET', 'POST'])
def train_data():
    if(request.get_json()['keyword'] is None):
        return "False"
    keyword = request.get_json()['keyword']
    get_data_from_fb(keyword)
    return render_template('index.html')

@dataset.route('/get_product', methods=['GET', 'POST'])
def get_product():  
    try:
        id_product = request.get_json()['id'] 
        token = request.get_json()['token']  
        if token and id_product and request.method == 'POST' and verify_login(token):  
            product = DataTrain.objects.get(id=id_product);

            # list_products = []
            # for item in products:  
            #     product = {
            #         "id":str(item.id),
            #         "title":item.title,
            #         "description":item.description,
            #         "image_file":item.image_file, 
            #         "author": item.author,
            #         "image_author": item.image_author,
            #         "like":item.like,
            #         "brand":item.brand,
            #         "date_posted":item.date_posted,
            #         "kind":item.kind,
            #         "url_page":item.url_page
            #     }  
            #     list_products.append(product)
            payload = {
                "product": product
            }  
            return json.dumps(Respone(True, payload, "GET PRODUCT SUCCESS"))   
        return json.dumps(Respone(False, {}, "GET PRODUCT FAILED"))  
    except:
        return json.dumps(Respone(False, {}, "Unauthorized"))   

@dataset.route('/get_products', methods=['GET', 'POST'])
def get_products():  
    # try:
    token = request.get_json()['token']  
    print( verify_login(token))
    if token and request.method == 'POST' and verify_login(token):   
        # page = request.get_json()['page'] 
        
        products = DataTrain.objects.all();

        list_products = []
        for item in products: 
            product = {
                "id":str(item.id),
                "title":item.title,
                "description":item.description,
                # "image_file":item.image_file, 
                "author": item.author,
                "image_author": item.image_author,
                "like":item.like,
                "brand":item.brand,
                "date_posted":item.date_posted,
                "kind":item.kind,
                "url_page":item.url_page,
                "url_image":item.url_image,
                "tags":item.tags,
                "age_data":item.age_data,
                "view":item.view,
                "price":item.price,
                "currency":item.currency
            }  
            list_products.append(product)
        payload = {
            "products": list_products
        }  
        return json.dumps(Respone(True, payload, "GET PRODUCTS SUCCESS"))   
        # return json.dumps(Respone(False, {}, "GET PRODUCTS FAILED"))  
    # except:
    return json.dumps(Respone(False, {}, "Unauthorized"))   

# @dataset.route('/get_products', methods=['GET', 'POST'])
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
# @users.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#         k = json.dumps(answers) 
#         return k
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
#         user = User(username=form.username.data, email=form.email.data,password=hashed_password)
#         user.save()
#         flash(f'Account created for {form.username.data}. Then, you can login Now', 'success')
#         return redirect(url_for('users.login'))
#     return render_template('register.html', title='Register', form=form)

# @users.route('/register', methods=['GET', 'POST'])
# def register():   
#     if current_user.is_authenticated: 
#         answer = Respone(False, {}, "User have been already login")
#         return json.dumps(answer) 
#     if request.method == 'POST':
#         username = request.get_json()['username']
#         email = request.get_json()['email']
#         password = request.get_json()['password']
#         role = request.get_json()['role']
 
#         user = User.objects.filter(email=email).first()
        
#         if not user: 
#             hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
#             user = User(username=username, email=email,password=hashed_password, role=role)
#             user.save()
            
#             payload = {
#                 "username":user.username,
#                 "email":user.email,
#                 "image_file":user.image_file,
#                 "role":user.role
#             } 
#             message = "Create User Success"
#             answer = Respone(True, payload, message)   
#         else:
#             answer = Respone(False, {}, "Email is exist")   
#         return json.dumps(answer) 
#     else:  
#         return render_template('index.html')

# @users.route('/login', methods=['GET', 'POST'])
# def login():     
#     if current_user.is_authenticated: 
#         answer = Respone(False, {}, "User have been already login")
#         return json.dumps(answer) 
#     if request.method == 'POST': 
#         info = request.get_json()['info']
#         type = request.get_json()['type']
#         if type == 'none':
#             email = info['email']
#             password = info['password']

#             user = User.objects.filter(email=email).first()
#             if user and bcrypt.check_password_hash(user.password, password): 
#                 login_user(user, remember=True) #save user login 
#                 token = user.get_login_token()
#                 payload = {
#                     "username":user.username,
#                     "email":user.email,
#                     "image_file":user.image_file,
#                     "role":user.role,
#                     "token": token,
#                     "type": "none"
#                 } 
#                 message="Login Successful"
#                 answer = Respone(True, payload, message)   
#             else:
#                 answer = Respone(False, {}, "Email or Password isn't correct")  
#         elif type == 'facebook': #login via facebook
#             id = info['userID']
#             user = User.objects.filter(email=id).first()

#             # user not yet availible
#             if not user: 
#                 username = info['name']
#                 role = 'customer'
#                 picture = info['picture']['data']['url']
#                 if picture:
#                     picture_file = save_picture(info['picture']['data']['url']) 
                    
#                 hashed_password = bcrypt.generate_password_hash(id).decode('utf-8') 
#                 user = User(username=username, email=id,password=hashed_password, role=role, image_file=picture_file,type=type)
#                 user.save()
            
#             login_user(user, remember=True) #save user login 
#             token = user.get_login_token()
            
#             payload = {
#                 "username":user.username,
#                 "email":user.email,
#                 "image_file":user.image_file,
#                 "role":user.role,
#                 "token": token,
#                 "type": type
#             }  
#             message="Login Successful"
#             answer = Respone(True, payload, message) 
#         elif type == 'google': #login via facebook
#             id = info['googleId']
#             email = info['email']
#             user = User.objects.filter(email=email).first()

#             # user not yet availible
#             if not user: 
#                 username = info['name']
#                 role = 'customer'
#                 pictureUrl = info['imageUrl']
#                 if pictureUrl:
#                     picture_file = save_picture(pictureUrl) 
                    
#                 hashed_password = bcrypt.generate_password_hash(id).decode('utf-8') 
#                 user = User(username=username, email=email,password=hashed_password, role=role, image_file=picture_file,type=type)
#                 user.save()
            
#             login_user(user, remember=True) #save user login 
#             token = user.get_login_token()

#             payload = {
#                 "username":user.username,
#                 "email":user.email,
#                 "image_file":user.image_file,
#                 "role":user.role,
#                 "token": token,
#                 "type": type
#             }  
#             message="Login Successful"
#             answer = Respone(True, payload, message) 
#         return json.dumps(answer)    
#     else:  
#         return render_template('index.html')

# @users.route("/logout")
# @login_required
# def logout():
#     if current_user.is_authenticated: 
#         logout_user()
#         answer = Respone(True, {}, "Logout Success")  
#         return json.dumps(answer)
#     return render_template('index.html')

# @users.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():  
#     if current_user.is_authenticated: 
#         answer = Respone(False, {}, "User have been already login")
#         return json.dumps(answer)  
#     if request.method == 'POST':
#         email = request.get_json()['email']
#         user = User.objects.filter(email=email).first()
#         if user:
#             send_reset_email(user)
#             answer = Respone(True, {}, "We sent a new password. Please check in your eamil")
#         else:
#             answer = Respone(False, {}, "We can't find your email. Please sign in first")
#         return json.dumps(answer) 
#     return render_template('index.html')

# @users.route('/get_users', methods=['GET', 'POST'])  
# def getAll():     
#     try: 
#         token = request.get_json()['token']  
#         if token and request.method == 'POST' and verify_login(token):   
#             list_user = User.objects.all();
#             users = []
#             for item in list_user:
#                 user = {
#                     "username":item.username,
#                     "email":item.email,
#                     "image_file":item.image_file,
#                     "role":item.role, 
#                     "type": item.type
#                 }  
#                 users.append(user)  
#             payload = {
#                 "users":users
#             }  
#             message="Get Users Successful" 
#             return json.dumps(Respone(True, payload, message)) 
#         return json.dumps(Respone(False, {}, "Get Users Failed"))
#     except:
#         return json.dumps(Respone(False, {}, "Unauthorized"))    

# @users.route('/get_user', methods=['GET', 'POST'])  
# def getByEmail():    
#     try: 
#         token = request.get_json()['token']  
#         if token and request.method == 'POST' and verify_login(token):   
#             email = request.get_json()['email'];
#             item = User.objects.filter(email=email).first();  
#             if item:
#                 user = {
#                     "username":item.username,
#                     "email":item.email,
#                     "image_file":item.image_file,
#                     "role":item.role, 
#                     "type": item.type
#                 }    
#                 payload = {
#                     "user":user
#                 }  
#                 message="Get User Successful" 
#                 return json.dumps(Respone(True, payload, message))
#         return json.dumps(Respone(False, {}, "Get User Failed"))
#     except:
#         return json.dumps(Respone(False, {}, "Unauthorized"))    
#     # logout_user() 
    


# @users.route("/reset_password_token", methods=['GET', 'POST'])
# def reset_token():  
#     password = request.get_json()['password']
#     token = request.get_json()['token']
#     if current_user.is_authenticated: 
#         answer = Respone(False, {}, "User have been already login")
#         return json.dumps(answer) 
#     user = User.verify_reset_token(token) 
#     if user is None:
#         answer = Respone(False, {}, "That is an valid or expired token")
#         return json.dumps(answer)   
#     if request.method == 'POST': 
#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8') 
#         user.password = hashed_password
#         user.save() 
#         answer = Respone(True, {}, "Your password have been updated! Then, you can login Now")
#         return json.dumps(answer)  
#     return render_template('index.html')

# @users.route('/token', methods=['GET', 'POST'])
# def check_token():
#     try: 
#         token = request.get_json()['token']  
#         if verify_login(token):   
#             return json.dumps(Respone(True, {}, "Authorized"))
#         return json.dumps(Respone(False, {}, "Unauthorized"))
#     except:
#         return json.dumps(Respone(False, {}, "Unauthorized"))