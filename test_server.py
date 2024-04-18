import sys
import io
from flask import Flask, render_template, Response, request, render_template_string, url_for, redirect

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def _main():
	if request.method == 'POST':
		print('POST')
		print(request.args.get('brand_name'))
	if request.method == 'GET':
		print('GET')
	return "ok"

if __name__ == '__main__':
	app.run(debug=True, port=5000)
