from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/api/list', methods=['GET'])
def show_reviews():
    reviews = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'result': 'success', 'reviews': reviews})

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/join')
def join():
    return render_template('join.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
