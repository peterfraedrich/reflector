#!/usr/bin/env python

import argparse
import yaml
from reflector.reflector import Reflector

# import config
with open('config.yaml', 'r') as c:
    config = yaml.load(c.read())

parser = argparse.ArgumentParser(description='REFLECTOR: splits HTTP into multiple backend servers')
parser.add_argument('--host', '--ip', '-i', default=config['server']['host'], help='Host to listen on; defaults to config setting')
parser.add_argument('--port', '-p', default=config['server']['port'], help='Port to listen on; defaults to config setting')
parser.add_argument('--debug', '-d', default=False, action='store_true', help='Enables debug mode; prints out some variables and such at app start.')
args = parser.parse_args()


if __name__ == '__main__':
    if args.debug:
        print '{:10} :: {}'.format('ARGS', args)
        print '{:10} :: {}'.format('CONFIG', config['upstream'])
    Reflector = Reflector(args, config)
    Reflector.start()