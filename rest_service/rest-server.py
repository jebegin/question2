#!/usr/bin/env python

from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

from proto.ip_event_pb2 import IpEvent

#{"sha_id":1,"count":12,"good_ips":2,"bad_ips":1}

events = {}
events['1'] = {'count':0,'good_ips':2,'bad_ips':1}
#events = [
#    {
#        'sha_id': 1,
#        'count': 12,
#        'good_ips': 2,
#        'bad_ips': 1
#    }
#]

@app.route('/events', methods=['GET'])
def get_events():
    return jsonify({'events': events})

@app.route('/events/<int:sha_id>', methods=['GET'])
def get_event(sha_id):
    sha = [sha for sha in events if sha['sha_id'] == sha_id]
    if len(sha) == 0:
        abort(404)
    return jsonify(sha[0])

@app.route('/events', methods=['POST'])
def create_event():
    #print 'Content-Type: %s' % request.headers['Content-Type']

    #if 'application/json' in request.headers['Content-Type']:
    #    event = {
    #        'sha_id': request.json['sha_id'],
    #        'count': request.json['count'],
    #        'good_ips': request.json['good_ips'],
    #        'bad_ips': request.json['bad_ips']
    #    }
    #    events.append(event)
    #    return jsonify({'event': event}), 201
    #else:
    #    abort(400)

    if 'application/octet-stream' in request.headers['Content-Type']:
        print 'data: %s' % request.data
        print 'form: %s' % request.form
        print 'values: %s' % request.values
        print 'files: %s' % request.files
                
        new_event = IpEvent()
        new_event.ParseFromString(request.data)
        print 'type: %s' % type(new_event)
        print 'new_event: %s' % new_event
        return 'figure out how to use proto'
        #event = {
        #    'sha_id': request.json['sha_id'],
        #    'count': request.json['count'],
        #    'good_ips': request.json['good_ips'],
        #    'bad_ips': request.json['bad_ips']
        #}
        #events.append(event)
        #return jsonify({'event': event}), 201
    else:
        abort(400)

@app.route('/events/<int:sha_id>', methods=['DELETE'])
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
