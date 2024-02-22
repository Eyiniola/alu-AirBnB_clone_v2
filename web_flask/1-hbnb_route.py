#!/usr/bin/python3
"""
a script that starts a Flask application
"""
from flask import Flask

app = Flask(__name__)

@app.route('/', '/hbnb', strict_slashes=False)
def hello_hbnb():
    return 'Hello HBNB'
def hbnb():
    return "HBNB"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
