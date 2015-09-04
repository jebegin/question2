#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

events = [
    {
        'sha_id': 1,
        'count': 12,
        'good_ips': 2,
        'bad_ips': 1
    }
]

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
    print 'Content-Type: %s' % request.headers['Content-Type']

    #if not request.json or not 'sha_id' in request.json:
    #    abort(400)
    #event = {
    #    'sha_id': request.json['sha_id'],
    #    'count': request.json['count'],
    #    'good_ips': request.json['good_ips'],
    #    'bad_ips': request.json['bad_ips']
    #}
    #events.append(event)
    #return jsonify({'event': event}), 201

    if 'application/octet-stream' in request.headers['Content-Type']:
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

#@app.route('/messages', methods = ['POST'])
#def api_message():
#
#    if request.headers['Content-Type'] == 'text/plain':
#        return "Text Message: " + request.data
#
#    elif request.headers['Content-Type'] == 'application/json':
#        return "JSON Message: " + json.dumps(request.json)
#
#    elif request.headers['Content-Type'] == 'application/octet-stream':
#        f = open('./binary', 'wb')
#        f.write(request.data)
#        f.close()
#        return "Binary message written!"
#
#    else:
#        return "415 Unsupported Media Type ;)"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
