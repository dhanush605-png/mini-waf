# backend.py
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Secure App"

@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username')
    return f"Hello {username}"

if __name__ == '__main__':
   app.run(port=5001, debug=True)