#!/usr/bin/env python

import sys
import json
import requests
from netaddr import IPNetwork, IPAddress
from proto.ip_event_pb2 import IpEvent
requests.packages.urllib3.disable_warnings()
from requests.exceptions import ConnectionError

def main(argv):

    
    r = requests.delete('http://localhost:5000/events')
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    print 'text: %s' % r.text

    print '--------------------'

    bad_ips = []
    ips = [IPAddress('192.168.1.16'), IPAddress('96.1.2.3'), IPAddress('223.5.76.1'), IPAddress('2.56.8.9'), IPAddress('96.1.2.3')]
    for ip in ips:
        event = IpEvent()
        event.app_sha256 = 'deadbeef'
        event.ip = ip.value
        bad_ips.append(event)

    for event in bad_ips:
        headers = {"Content-Type":"application/octet-stream"}    
        r = requests.post(
            'http://localhost:5000/events',
            headers=headers,
            data=event.SerializeToString())
        print 'url: ' + r.url
        print 'status: %s' % r.status_code
        if r.status_code == 201 or r.status_code == 200:
            print 'headers: %s' % r.headers
            print 'text: %s' % r.text
        
    print '--------------------'

    good_ips = []
    # good IPs
    for ip in IPNetwork('192.168.1.0/28').iter_hosts():
        event = IpEvent()
        event.app_sha256 = 'deadbeef'
        event.ip = ip.value
        good_ips.append(event)

    event = IpEvent()
    event.app_sha256 = 'deadbeef'
    event.ip = IPAddress('192.168.1.1').value
    good_ips.append(event)


    for event in good_ips:
        headers = {"Content-Type":"application/octet-stream"}    
        r = requests.post(
            'http://localhost:5000/events',
            headers=headers,
            data=event.SerializeToString())
        print 'url: ' + r.url
        print 'status: %s' % r.status_code
        if r.status_code == 201 or r.status_code == 200:
            print 'headers: %s' % r.headers
            print 'text: %s' % r.text
    
    print '--------------------'
    
    bad_ips = []
    ips = [IPAddress('96.1.2.3'), IPAddress('223.5.76.1'), IPAddress('2.56.8.9'), IPAddress('96.1.2.3')]
    for ip in ips:
        event = IpEvent()
        event.app_sha256 = 'deadbeef'
        event.ip = ip.value
        bad_ips.append(event)
    
    for event in bad_ips:
        headers = {"Content-Type":"application/octet-stream"}    
        r = requests.post(
            'http://localhost:5000/events',
            headers=headers,
            data=event.SerializeToString())
        print 'url: ' + r.url
        print 'status: %s' % r.status_code
        if r.status_code == 201 or r.status_code == 200:
            print 'headers: %s' % r.headers
            print 'text: %s' % r.text
    
    print '--------------------'

    ip = IPNetwork('192.168.1.1/28')
    
    event1 = IpEvent()
    event1.app_sha256='123fff'
    event1.ip=ip.value    
    print 'event: %s' % event1
    
    event2 = IpEvent()
    event2.app_sha256='123aaa'
    event2.ip=ip.value
    print 'event: %s' % event2
    
    print '--------------------'
        
    headers = {'Accept':'application/json'}
    r = requests.get('http://localhost:5000/events/123fff', headers=headers)
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    print 'headers: %s' % r.headers
    print 'text: %s' % r.text
    print 'json response: %s' % r.json()
    
    print '--------------------'
    
    headers = {"Content-Type":"application/octet-stream"}    
    r = requests.post(
        'http://localhost:5000/events',
        headers=headers,
        data=event1.SerializeToString())
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    if r.status_code == 201 or r.status_code == 200:
        print 'headers: %s' % r.headers
        print 'text: %s' % r.text
        #print 'json response: %s' % r.json()
    
    print '--------------------'
    
    headers = {"Content-Type":"application/octet-stream"}    
    r = requests.post(
        'http://localhost:5000/events',
        headers=headers,
        data=event1.SerializeToString())
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    if r.status_code == 201 or r.status_code == 200:
        print 'headers: %s' % r.headers
        print 'text: %s' % r.text
        #print 'json response: %s' % r.json()
    
    print '--------------------'
    
    headers = {"Content-Type":"application/octet-stream"}    
    r = requests.post(
        'http://localhost:5000/events',
        headers=headers,
        data=event2.SerializeToString())
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    if r.status_code == 201 or r.status_code == 200:
        print 'headers: %s' % r.headers
        print 'text: %s' % r.text
        #print 'json response: %s' % r.json()
    
    print '--------------------'
    
    headers = {'Accept':'application/json'}
    r = requests.get('http://localhost:5000/events/123fff', headers=headers)
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    print 'headers: %s' % r.headers
    print 'text: %s' % r.text
    print 'json response: %s' % r.json()
    
    print '--------------------'
    
    headers = {'Accept':'application/json'}
    r = requests.get('http://localhost:5000/events/123aaa', headers=headers)
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    print 'headers: %s' % r.headers
    print 'text: %s' % r.text
    print 'json response: %s' % r.json()
    
    print '--------------------'
    
    headers = {'Accept':'application/json'}
    r = requests.get('http://localhost:5000/events/deadbeef', headers=headers)
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    print 'headers: %s' % r.headers
    print 'text: %s' % r.text
    print 'json response: %s' % r.json()
    
    print '--------------------'

    headers = {'Accept':'application/json'}
    r = requests.get('http://localhost:5000/events/123aaa', headers=headers)
    print 'url: ' + r.url
    print 'status: %s' % r.status_code
    print 'headers: %s' % r.headers
    print 'text: %s' % r.text
    print 'json response: %s' % r.json()
    
    print '--------------------'

if __name__ == '__main__':
    main(sys.argv[1:])
