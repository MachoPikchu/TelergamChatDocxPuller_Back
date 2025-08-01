from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)

# ✅ Enable CORS only for your Netlify site
CORS(app, origins=["https://shadowslavereader.netlify.app"])

@app.route('/')
def root():
    return "ShadowSlave chapter server is running!"

@app.route('/chapters')
def chapters():
    if not os.path.exists('chapters.json'):
        return jsonify([])
    with open('chapters.json', encoding='utf-8') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
