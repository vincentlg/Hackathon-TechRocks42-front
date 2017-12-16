from flask import Flask, jsonify, request, current_app, render_template
from bs4 import BeautifulSoup
import urllib
import sys
from urllib.request import Request, urlopen
import re
import json
from flask_restful import Resource, Api
import os

app = Flask(__name__)
api = Api(app)

class Data(Resource):
    def get(self):
        with open('data.json', 'r') as f:
            data = json.load(f)
        return data

@app.route('/')
def index():
    return render_template('./web/index.html')

@app.route('/game')
def test():
    first = request.args.get('first', '')
    second = request.args.get('second', '')
    print(first)
    print(second)
    os.system('python3 scrapper.py ' + first + ' ' + second)
    api.add_resource(Data, '/data')

if __name__ == '__main__':
    app.run(debug=True)
