#!/usr/bin/env python3

import os
import datetime

from flask import Flask, render_template, request, jsonify, send_from_directory
from pyawair import awair

try:
    from secret import AWAIR_USERNAME, AWAIR_PASSWORD
except ImportError:
    print('Failed to load secret.py')


app = Flask(__name__, static_url_path='/static')

if os.getenv('APPLICATION_ROOT'):
    app.config['APPLICATION_ROOT'] = os.getenv('APPLICATION_ROOT')

cors_origins = '*'
if os.getenv('CORS_ALLOWED_ORIGINS'):
    cors_origins = os.getenv('CORS_ALLOWED_ORIGINS').split(',')

# Log messages with Gunicorn
if not app.debug:
    import logging
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

api = awair(AWAIR_USERNAME, AWAIR_PASSWORD)
device = api.devices()[0]
app.logger.info('Device: %s' % device)

@app.route('/')
def index():
    return render_template('index.html', mini=request.args.get('mini', False))

@app.route('/api/events_score')
def events_score():
    data = api.timeline(device)
    if data:
        return jsonify([data[-1]])
    return jsonify([{}])

@app.route('/api/inbox_items')
def inbox_items():
    data = api.inbox_items(device, limit=request.args.get('limit', 1))
    return jsonify(data)

@app.route('/static/<path:path>')
def static_path(path):
    return send_from_directory('static', path)
