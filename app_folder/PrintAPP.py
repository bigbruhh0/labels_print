import subprocess
import requests
import tkinter as tk
from datetime import datetime

f=open('conf.ini', "w")
url = 'http://127.0.0.1:5000/'
server_path = 'server_holder.py'

def check_date():
	current_datetime = datetime.now()
	current_date = current_datetime.date()
	print("Текущая дата:", current_date)
	day=current_datetime.day
	print(day)
	global cur_day
	cur_day=day
	
last_day=0
cur_day=0
def read_info():
	file_path = "config/data.txt"

	# Открыть файл для чтения и записи
	with open(file_path, 'r+') as file:
		# Считать первую строку из файла
		first_line = file.readline().strip()
	global last_day
	last_day=int(first_line)
	
read_info()
print(last_day)

def send_post_request():
    brand_name = brand_name_entry.get()
    frag_name = frag_name_entry.get()
    conc = conc_entry.get()
    ml = ml_entry.get()
    requests.post(url,data={'brand_name':brand_name, 'frag_name':frag_name, 'conc':conc, 'ml':ml,'type':1})
    result_label.config(text='POST request sent')

def send_get_request():
    result_label.config(text='GET request sent')
    
check_date()

if cur_day==last_day:
	print('Продолжение сессии')
	print('Файл:')
	pass
if cur_day!=last_day:
	file_name=datetime.now().date()
	print(file_name)
	print('Новая сессия')
	print('Файл:')
	pass

root = tk.Tk()
root.title("Server Control App")

#start_button = tk.Button(root, text="Включить сервер", command=start_server)
send_post_button = tk.Button(root, text="Отправить POST запрос", command=send_post_request)
send_get_button = tk.Button(root, text="Отправить GET запрос", command=send_get_request)

brand_name_entry = tk.Entry(root, width=30)
brand_name_entry.insert(0, "Brand Name")

frag_name_entry = tk.Entry(root, width=30)
frag_name_entry.insert(0, "Frag Name")

conc_entry = tk.Entry(root, width=30)
conc_entry.insert(0, "Conc")

ml_entry = tk.Entry(root, width=30)
ml_entry.insert(0, "ML")

result_label = tk.Label(root, text="")

#start_button.grid(row=0, column=0, pady=5)
send_post_button.grid(row=1, column=0, pady=5)
send_get_button.grid(row=1, column=1, pady=5)
brand_name_entry.grid(row=2, column=0, columnspan=2, pady=5)
frag_name_entry.grid(row=3, column=0, columnspan=2, pady=5)
conc_entry.grid(row=4, column=0, columnspan=2, pady=5)
ml_entry.grid(row=5, column=0, columnspan=2, pady=5)
result_label.grid(row=6, column=0, columnspan=2)

root.mainloop()
