"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask import jsonify
from flask import make_response
from flask import url_for
from flask import request
from flask import abort
from collections import OrderedDict 
import camera
app = Flask(__name__)
auth = HTTPBasicAuth()
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

users = {
    "user": "user",
    "admin": "admin"
}

#Авторизация с именем-паролем
@auth.get_password
def get_password(username):
    if username in users:
        return users.get(username)
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({ 'error': 'Unauthorized access' }), 403)
    
    
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error= (e.description)), 404
   

@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(error= (e.description)), 400

@app.errorhandler(405)
def resource_not_found(e):
    return jsonify(error= (e.description)), 405


@app.route('/check', methods=['GET', 'POST'])
@auth.login_required
def check():
    if request.method == 'GET':
        abort(405, description="Method Not Allowed")
    if not request.json:
        abort(400, description="Resource not json")        

    #Проверяем протокол в запросе
    if not 'protocol' in request.json:
        abort(400, description="Protocol not found")
    protocol = request.json.get('protocol')

    # Проверяем ip адрес камеры в запросе
    if not 'ip' in request.json:
        abort(400, description="IP not found")

    ip = request.json.get('ip')
    if not validate_ip(ip):
        abort(400, description="IP is not correct")

    # Проверяем порт камеры в запросе
    if not 'port' in request.json:
        abort(400, description="Port not found")
    port = request.json.get('port')
    if not RepresentsInt(port):
        abort(400, description="Port must be integer")

    # Проверяем путь до видео в запросе
    if not 'path' in request.json:
        path = ''
    else:
        path = '/{0}'.format(request.json.get('path'))

    userpass = ''
    if 'user' in request.json and 'pass' in request.json:
        userpass = '{0}:{1}@'.format(request.json.get('user'), request.json.get('pass'))
    else:
        abort(400, description="Check user and pass in json")
    source = '{0}://{1}{2}:{3}{4}'.format(protocol, userpass, ip, port, path)
    data = OrderedDict({'ip': ip, 'port': port, 'protocol': protocol, 'source': source})

    #Проверяем камеру на доступность
    check = camera.Checks(source)
    if not check.testDevice():
        data.update({'Error': 'Camera is not available'})
    else:
        data.update({'status': 'Camera is available'})
        data.update(check.testFrames())
    return data

#Валидация ip адреса
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

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
