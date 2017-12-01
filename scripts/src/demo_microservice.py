#!flask/bin/python
from __future__ import print_function
import sys, json, traceback
from flask import Flask, jsonify, request, make_response, abort
import demo_subcurrency

"""
RESTful web service endpoints using Flask.
"""
app = Flask(__name__)

@app.route('/api/v1.0/query', methods=['GET'])
def get_query():
    """
    Examples:
      - curl -i "http://localhost:5000/api/v1.0/query?query=None&median_balance=True"
    """
    print("Called get_query with request in microservice.py: %r" % (json.dumps(request.json, indent=4, sort_keys=True)))
    sys.stdout.flush() # Capture in logs
    query_params = request.args.to_dict()
    if len(query_params) == 0:
        abort(400)
    print("Query Params: ", query_params, file=sys.stderr)

    data = demo_subcurrency.get_or_set_blockchain_data('blockchain_data', None)
    # response = {'success':True}
    response = {
        "longest_chain": data
    }
    return jsonify(response), 200, {'ContentType':'application/json'}

@app.route('/', methods=['POST'])
def post_messages():
    """
    Handles messages from Client DApp

    curl -i -X POST "http://localhost:5000/api/v1.0/query?query=None&address_from=None&address_to=None&amount=None"
    """
    try:
        print("Called post_messages in microservice.py")
        response_data = request.json
        print('Received message: %r' % (json.dumps(response_data, indent=4, sort_keys=True)))
    except Exception as e:
        traceback.print_exc()
        e = sys.exc_info()[0]
        print(e)
        print("Error handling incoming message at line: " + str(sys.exc_traceback.tb_lineno))
        return False
    return True

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def run():
    app.run(host='127.0.0.1', port=5000, debug=True, use_debugger=False, use_reloader=False)

if __name__ == '__main__':
    run()