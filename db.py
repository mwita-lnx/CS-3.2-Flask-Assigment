import pymongo
import smtplib
from email.mime.text import MIMEText
import random
import string
from flask import request, url_for

client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
userdb = client['userdb']
users = userdb.customers

def insert_data():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        address = request.form['address']
        reg_number = request.form['reg_number']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['pass']

        reg_user = {
            'username': username,
            'name': name,
            'address': address,
            'reg_number': reg_number,
            'phone': phone,
            'email': email,
            'password': password
        }

        # Check if username or email already exists
        if users.find_one({"$or": [{"username": username}, {"email": email}]}) == None:
            users.insert_one(reg_user)
            return True
        else:
            return False

def check_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['pass']

        user = {
            "username": username,
            "password": password
        }

        user_data = users.find_one(user)
        if user_data == None:
            return False, ""
        else:
            return True, user_data["name"]

def search_users(reg_number=None):
    """Search users by registration number. If no reg_number is provided, return all users."""
    try:
        if reg_number:
            query = {"reg_number": {"$regex": reg_number, "$options": "i"}}
            cursor = users.find(query, {'password': 0})
        else:
            cursor = users.find({}, {'password': 0})
        
        # Convert cursor to list and handle MongoDB objects
        users_list = list(cursor)
        return users_list
    except Exception as e:
        print(f"Search error: {e}")
        return []

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=50))

def send_reset_email(email):
    print(email)
    user = users.find_one({"email": email})
    print(user)
    if not user:
        return False
    
    token = generate_token()
    users.update_one({"email": email}, {"$set": {"reset_token": token}})

    print(token)
    
    reset_link = url_for('reset_password', token=token, _external=True)
    
    your_email= 'amiremir346@gmail.com'
    receipient_email=email
    subject="Reset password email"
    msg = MIMEText(f"Click the link to reset your password: {reset_link}")
    text=f"Subject: {subject}\n\n{msg}"

    print(msg)
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(your_email,'fpfthcetaetnuexr')
        server.sendmail(your_email,receipient_email,text)
        return True
    except Exception as e:
        print(f"SMTP error: {e}")
        return False
def reset_password(token, new_password):
    user = users.find_one({"reset_token": token})
    if not user:
        return False
    
    users.update_one({"reset_token": token}, {"$set": {"password": new_password, "reset_token": None}})
    return True
