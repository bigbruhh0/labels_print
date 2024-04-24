import sys
import io
from flask import Flask, render_template, Response, request, render_template_string, url_for, redirect
import subprocess
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def _main():
	if request.method == 'POST':
		print('POST')
		_type = request.form.get('type')  # Изменено на request.form
		brand_name = request.form.get('brand_name')
		frag=request.form.get('frag_name')
		frag_name = frag
		conc = request.form.get('conc')
		ml = request.form.get('ml')

		if None in [brand_name, frag_name, conc, ml]:
			print("Одно из значений не было получено.")
			return "Не все данные предоставлены", 400

		# Здесь вставьте вызов subprocess с проверкой None перед вызовом
		subprocess.run(['python', 'new_life.py', brand_name, frag_name, conc, ml], check=True)
		print(brand_name, frag_name, conc, ml)

	if request.method == 'GET':
		print('GET')

	return brand_name+'_'+frag_name+'_'+conc+"_"+ml+' '+"ok"

if __name__ == '__main__':
	app.run(debug=True, port=5000)
