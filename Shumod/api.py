from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
import sys

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'hack':
        return 'aton'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


@app.errorhandler(400)
def not_found(error):
    return jsonify(error=str(error)), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404


@app.route('/check', methods=['POST'])
@auth.login_required
def check():
    if not request.json or not 'ip' in request.json:
        abort(400, description="IP not found")

    ip = request.json.get('ip')
    if not validate_ip(ip):
        abort(400, description="IP is not correct")

    if not request.json or not 'port' in request.json:
        abort(400, description="Port not found")
    port = request.json.get('port')
    if not isinstance(port, int):
        abort(400, description="Port must be integer")

    return {'ip': ip, 'port': port}


def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


if __name__ == '__main__':
    port = 5556
    #Возможность запустить сразу с номером порта: python api.py 1111
    if (sys.argv.__len__() > 1):
        port = sys.argv[1]

    app.run(port=port, debug=True)
