#!/usr/bin/env python

from flask import Flask
from flask import request
import argparse
app = Flask(__name__)

parser = argparse.ArgumentParser(description='Testing web server')
parser.add_argument('--host', '--ip', '-i', default='0.0.0.0')
parser.add_argument('--port', '-p', default='9000')
args = parser.parse_args()

@app.route('/')
@app.route('/<uri>')
def root():
    print request.__dict__
    return '200 OK\n'

@app.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def test():
    print request.__dict__
    return '200 OK\n'

app.run(host=args.host, port=args.port, threaded=True)