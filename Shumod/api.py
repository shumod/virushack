from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
import sys
from Shumod import video

app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()

#Авторизация с именем-паролем
@auth.get_password
def get_password(username):
    if username == 'hack':
        return 'aton'
    return None

#Обработка ошибок
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)

@app.errorhandler(400)
def not_found(error):
    return jsonify(error=str(error)), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404

#Роут для проверки камеры
@app.route('/check', methods=['POST'])
@auth.login_required
def check():
    if not request.json:
        abort(400, description="Request not found")

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
    if not isinstance(port, int):
        abort(400, description="Port must be integer")

    # Проверяем путь до видео в запросе
    if not 'path' in request.json:
        path = ''
    else:
        path = '/{0}'.format(request.json.get('path'))

    userpass = ''
    if 'user' in request.json and 'pass' in request.json:
        userpass = '{0}:{1}@'.format(request.json.get('user'), request.json.get('pass'))

    source = '{0}://{1}{2}:{3}{4}'.format(protocol, userpass, ip, port, path)

    data = {'ip': ip, 'port': port, 'protocol': protocol, 'source': source}

    #Проверяем камеру на доступность
    check = video.Checks(source)
    if not check.testDevice():
        data['error'] = 'Camera is not available'

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


if __name__ == '__main__':
    port = 5556
    #Возможность запустить сразу с номером порта: python api.py 1111
    if (sys.argv.__len__() > 1):
        port = sys.argv[1]

    app.run(port=port, debug=True)
