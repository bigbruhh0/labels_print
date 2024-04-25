import sys
import socket
from flask import Flask, request
import subprocess

app = Flask(__name__)
server_started = False

def exit_app():
    sys.exit()

@app.route('/', methods=['GET', 'POST'])
def _main():
    if request.method == 'POST':
        print('POST')
        _type = request.form.get('type')
        print(_type, 'type')
        if _type == '1':
            brand_name = request.form.get('brand_name')
            frag = request.form.get('frag_name')
            frag_name = frag
            conc = request.form.get('conc')
            ml = request.form.get('ml')

            if None in [brand_name, frag_name, conc, ml]:
                print("Одно из значений не было получено.")
                return "Не все данные предоставлены", 400

            subprocess.run(['python', 'new_life.py', brand_name, frag_name, conc, ml], check=True)
            print(brand_name, frag_name, conc, ml)

    if request.method == 'GET':
        print('GET')

    return brand_name + '_' + frag_name + '_' + conc + "_" + ml + ' ' + "ok"

@app.route('/shutdown', methods=['POST'])
def shutdown_server():
	print('SHUTDOWN')
	global server_started
	if not server_started:
		raise RuntimeError('Сервер не запущен')

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.connect(('localhost', 5000))
	server_socket.send(b'Shutdown')
	server_socket.close()
	print('Сервер выключен')
	return 'Сервер выключен'

if __name__ == '__main__':
    server_started = True
    app.run(debug=True, port=5000)
