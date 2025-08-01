from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

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
    app.run(host='0.0.0.0', port=10000)  # Render uses dynamic ports via env if needed
