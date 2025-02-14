import smtplib
from email.mime.text import MIMEText
import db
import json
from flask import Flask, request, render_template, jsonify, url_for, session, redirect
from bson import json_util  # Add this import for MongoDB object serialization
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("signInUp.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    status, username = db.check_user()
    if status:
        session['username'] = username
        data = {
            "username": username,
            "status": status
        }
        return json.dumps(data)
    return json.dumps({"status": False})

@app.route('/logout', methods=['POST'])  # Add POST to methods
def logout():
    session.clear()  # Clear all session data, not just username
    return jsonify({"redirect": url_for('home')})  # Return JSON response with redirect URL

@app.route('/register', methods=['GET', 'POST'])
def register():
    status = db.insert_data()
    return json.dumps(status)

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('home'))
    return render_template("dash.html")

@app.route('/api/search', methods=['GET'])
def search():
    try:
        reg_number = request.args.get('reg_number', '')
        users = db.search_users(reg_number if reg_number else None)
        # Convert MongoDB objects to JSON-serializable format
        return json.dumps(users, default=json_util.default)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        status = db.send_reset_email(email)
        return json.dumps({"status": status})
    return render_template("forgot_password.html")

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):

    if request.method == 'POST':
        new_password = request.form['new_password']
        status = db.reset_password(token, new_password)
        return json.dumps({"status": status})
    return render_template("reset_password.html", token=token)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)