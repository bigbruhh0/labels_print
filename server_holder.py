import sys
import io
from flask import Flask, render_template, Response, request, render_template_string, url_for, redirect
import subprocess
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def _main():
	if request.method == 'POST':
		print('POST')
		_type=request.args.get('type')
		brand_name=request.args.get('brand_name')
		frag_name=request.args.get('frag_name')
		conc=request.args.get('conc')
		ml=request.args.get('ml')
		subprocess.run(['python', 'get_pdf.py',brand_name,frag_name,conc,ml])
		print(brand_name,frag_name,conc,ml)
	if request.method == 'GET':
		print('GET')
	return "ok"

if __name__ == '__main__':
	app.run(debug=True, port=5000)
