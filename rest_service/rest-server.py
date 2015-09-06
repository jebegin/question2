#!/usr/bin/env python

from flask import Flask, jsonify, abort, make_response, request
from proto.ip_event_pb2 import IpEvent
from netaddr import IPAddress

app = Flask(__name__)

app_shas = {}
app_shas['123fff'] = {'count':0,'good_ips':2,'bad_ips':1}

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
        else:
            app_shas[sha_id]={'count':1,'good_ips':0,'bad_ips':0}
            print app_shas
        
        return 'figure out how to use proto'
        #return jsonify({'event': event}), 201
    else:
        abort(400)

@app.route('/events/<sha_id>', methods=['DELETE'])
def delete_task(sha_id):
    sha = [sha for sha in events if sha['sha_id'] == sha_id]
    if len(sha) == 0:
        abort(404)
    events.remove(sha[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
