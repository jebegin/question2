#!/usr/bin/env python

from flask import Flask, jsonify, abort, make_response, request
from proto.ip_event_pb2 import IpEvent
from netaddr import IPAddress, IPSet

app = Flask(__name__)

app_shas = {}

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify(app_shas)

@app.route('/events/<sha_id>', methods=['GET'])
def get_event(sha_id):
    if 'application/json' in request.headers['Accept']:
        try:
            app_shas[sha_id]
        except KeyError:
            abort(404)
        else:
            return jsonify(app_shas[sha_id])
    else:
        abort(404)

@app.route('/events', methods=['POST'])
def create_event():
    if 'application/octet-stream' in request.headers['Content-Type']:

        event = IpEvent()
        event.ParseFromString(request.data)
        sha_id = str(event.app_sha256)
        ip = str(IPAddress(event.ip))
        
        if sha_id in app_shas:
            app_shas[sha_id]['count'] = app_shas[sha_id]['count'] + 1
            app_shas[sha_id]['good_ips'].append(ip)
        else:
            app_shas[sha_id]={'count':1,'good_ips':[],'bad_ips':[]}
            app_shas[sha_id]['good_ips'].append(ip)
        
        ips = app_shas[sha_id]['good_ips'] + app_shas[sha_id]['bad_ips']
        ip_set = IPSet(ips)
        for ip_range in ip_set.iter_ipranges():
            print ip_range
            print ip_range.size
            if ip_range.size == 14:
                good_range = ip_range
        
        for ip in good_range:
            print ip, ip in ip_set
        
        
        return 'Received event...'
    else:
        abort(400)

@app.route('/events', methods=['DELETE'])
def delete_events():

    app_shas.clear()    
    return jsonify({'result': True})

@app.route('/events/<sha_id>', methods=['DELETE'])
def delete_event(sha_id):
    try:
        del app_shas[sha_id]
    except KeyError:
        abort(404)
    else:
        return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
