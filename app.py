import db
import json
from flask import Flask, request, render_template, jsonify
from bson import json_util  # Add this import for MongoDB object serialization

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("signInUp.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    status, username = db.check_user()
    data = {
        "username": username,
        "status": status
    }
    return json.dumps(data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    status = db.insert_data()
    return json.dumps(status)

@app.route('/dashboard', methods=['GET'])
def dashboard():
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

if __name__ == '__main__':
    app.run(debug=True)