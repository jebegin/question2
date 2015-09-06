#!/usr/bin/env python

import sys
import json
import requests
from netaddr import IPNetwork
from proto.ip_event_pb2 import IpEvent
requests.packages.urllib3.disable_warnings()
from requests.exceptions import ConnectionError

def main(argv):
    
    ip = IPNetwork('192.168.1.1/28')
    
    event = IpEvent()
    event.app_sha256='123fff'
    event.ip=ip.value
    
    print 'event: %s' % event
    
    r = requests.get('http://localhost:5000/events')
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    print 'headers: %s' % r.headers
    print 'text: %s' % r.text
    print 'json response: %s' % r.json()
    
    print
    
    headers = {'Accept':'application/json'}
    r = requests.get('http://localhost:5000/events/123fff', headers=headers)
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    print 'headers: %s' % r.headers
    print 'text: %s' % r.text
    print 'json response: %s' % r.json()
    
    print

    headers = {"Content-Type":"application/octet-stream"}    
    r = requests.post('http://localhost:5000/events', headers=headers, data=event.SerializeToString())
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    if r.status_code == 201 or r.status_code == 200:
        print 'headers: %s' % r.headers
        print 'text: %s' % r.text
        #print 'json response: %s' % r.json()

    print

    headers = {'Accept':'application/json'}
    r = requests.get('http://localhost:5000/events/123fff', headers=headers)
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    print 'headers: %s' % r.headers
    print 'text: %s' % r.text
    print 'json response: %s' % r.json()
    
    print

    #r = requests.delete('http://localhost:5000/events/5')
    #print 'url: ' + r.url
    #print 'status: %s' % r.status_code
    #print 'text: %s' % r.text


if __name__ == '__main__':
    main(sys.argv[1:])
