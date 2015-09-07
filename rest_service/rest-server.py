#!/usr/bin/env python

from flask import Flask, jsonify, abort, make_response, request
from proto.ip_event_pb2 import IpEvent
from netaddr import IPAddress, IPSet

app = Flask(__name__)

app_shas = {}

@app.route('/events', methods=['GET'])
def get_events():
    """
    Return all events descriptions for all app_sha256 values
    """
    if 'application/json' in request.headers['Accept']:
        return jsonify(app_shas)

@app.route('/events/<sha_id>', methods=['GET'])
def get_event(sha_id):
    """
    Return event description for specified app_sha_256
    """
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
    """
    Updating event descriptions for an app_sha256.  Assuming all IPs are good
    untl at least a range of IPs reaches 14 (/28 network block).  Once a range
    of IPs reaches a total of 14, all other IPs are considered bad.  If
    multiple ranges of IPs reach 14, this simple processing will not be able to
    determine while /28 block is the valid one.
    """
    if 'application/octet-stream' in request.headers['Content-Type']:

        # Protobuf decoding
        event = IpEvent()
        event.ParseFromString(request.data)
        sha_id = str(event.app_sha256)
        ip = str(IPAddress(event.ip))
        
        # Update event description of an existing app_sha256
        if sha_id in app_shas:
            app_shas[sha_id]['count'] = app_shas[sha_id]['count'] + 1
            # Only add if IP is not already in the list
            if str(ip) not in app_shas[sha_id]['good_ips']:
                app_shas[sha_id]['good_ips'].append(str(ip))
        # Create an event description instance for a new app_sha256
        else:
            app_shas[sha_id]={'count':1,'good_ips':[],'bad_ips':[]}
            # Only add if IP is not already in the list
            if str(ip) not in app_shas[sha_id]['good_ips']:
                app_shas[sha_id]['good_ips'].append(str(ip))
        
        # Combined list of all IPs good and bad
        ips = app_shas[sha_id]['good_ips'] + app_shas[sha_id]['bad_ips']
        # Convert to a set
        ip_set = IPSet(ips)
        # Get the minimal number of IP ranges
        for ip_range in ip_set.iter_ipranges():
            # Does one of te ranges have 14 IP address in it?
            if ip_range.size == 14:
                # Thas is now our good /28 block of IP addresses
                good_range = ip_range
                app_shas[sha_id]['good_ips'] = []

                for ip in ip_set:
                    # Populate good_ips with the range of 14 'good' IP addresses
                    if ip in good_range:
                        if str(ip) not in app_shas[sha_id]['good_ips']:
                            app_shas[sha_id]['good_ips'].append(str(ip))
                    # Put the rest of IP addresses in bad_ips
                    else:
                        if str(ip) not in app_shas[sha_id]['bad_ips']:
                            app_shas[sha_id]['bad_ips'].append(str(ip))
        
        return 'Received event...'
    else:
        abort(400)

@app.route('/events', methods=['DELETE'])
def delete_events():
    """
    Delete all app_sha256 event description data
    """
    app_shas.clear()    
    return jsonify({'result': True})

@app.route('/events/<sha_id>', methods=['DELETE'])
def delete_event(sha_id):
    """
    Delete specified app_sha256 event descriptions
    """
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
