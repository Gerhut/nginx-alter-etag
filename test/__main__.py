#!/usr/bin/env python

import requests

def parse_etag(etag):
    if etag.startswith('W/'): # Weak etag
        etag = etag[2:]
    assert etag.startswith('"') and etag.endswith('"')
    return etag[1:-1]

def to_etag(value):
    return 'W/"{}"'.format(value)

nginx_etag = requests.get('http://nginx/').headers['etag']
node_etag = requests.get('http://node/').headers['etag']

print('nginx etag', nginx_etag)
print('node etag', node_etag)

nginx_etag = parse_etag(nginx_etag)
node_etag = parse_etag(node_etag)

vbar_index = nginx_etag.rindex('|')
upstream_etag = nginx_etag[:vbar_index]
proxy_etag = nginx_etag[vbar_index+1:]

print('proxy etag value', proxy_etag)
print('upstream etag value', upstream_etag)

assert node_etag == upstream_etag

assert requests.get('http://node/', headers={
  'If-None-Match': to_etag(upstream_etag)
}).status_code == 304

assert requests.get('http://nginx/', headers={
  'If-None-Match': to_etag('{}|{}'.format(upstream_etag, proxy_etag))
}).status_code == 304

assert requests.get('http://nginx/', headers={
  'If-None-Match': to_etag('{}|{}'.format(upstream_etag + 'P', proxy_etag))
}).status_code == 200

assert requests.get('http://nginx/', headers={
  'If-None-Match': to_etag('{}|{}'.format(upstream_etag, proxy_etag + 'P'))
}).status_code == 200
