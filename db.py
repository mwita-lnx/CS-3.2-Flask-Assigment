import pymongo
from flask import request
from bson import json_util

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