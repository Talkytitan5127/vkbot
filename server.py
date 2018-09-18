#!/usr/bin/python3

# flask-server, process requests from vk server
import logging
import requests
import os

from flask import Flask, request, jsonify
from werkzeug.contrib.fixers import ProxyFix

import bot

app = Flask(__name__)

request_form = 'https://api.vk.com/method/{}'

@app.route('/')
def index():
    return "Index method"

@app.route('/vkapi', methods=['POST'])
def getData():
    data = request.json
    app.logger.debug(data)
    if data['type'] == 'confirmation' and data['group_id'] == os.environ['group_id']:
        return os.environ['access_string']

    # process responce
    app.logger.debug(bot.run(data, make_request))

    # send answer
    return "ok"

def generate_params(params):
    data = {
        'access_token': os.environ['TOKEN'],
        'v': 5.84,
    }
    data.update(params)
    return data

def make_request(method, data):
    response = requests.get(
        request_form.format(method),
        params=generate_params(data)
    )
    return response.json()

app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.run(host='0.0.0.0', port=8000, debug=True)
