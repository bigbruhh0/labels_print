import subprocess
import requests
import tkinter as tk
from datetime import datetime

def check_date():
	current_datetime = datetime.now()
	current_date =current_datetime.strftime("%d-%m-%Y")
	print("Текущая дата:", current_date)
	day=current_datetime.day
	return current_date
	
def read_info(f_path):
	with open(f_path, "r") as file:
		lines = [line.strip() for line in file.readlines()]
	kek=[]
	for i in lines:
		p=i.find('|')
		kek.append(i)
	return kek

def send_post_request():
	_copy=1
	brand_name = brand_name_entry.get()
	frag_name = frag_name_entry.get()
	conc = conc_entry.get()
	ml = ml_entry.get()
	#requests.post(url,data={'brand_name':brand_name.replace('№','NO '), 'frag_name':frag_name.replace('№','NO '), 'conc':conc, 'ml':ml,'type':1})
	result_label.config(text='POST request sent')
	add_work(brand_name.upper()+'_'+frag_name+'_'+conc+'_'+ml)
	number_label.config(text=str(len(done_work)))
    
def add_work(text):
	global done_work
	current_datetime = datetime.now()
	hms = current_datetime.strftime("%H:%M:%S")
	text=hms+'|'+text.replace(' ','_')
	print('ADD:',text)
	done_work.append(text)
	with open(file_path, "w") as file:
		for i in range(len(done_work)):
			file.write(done_work[i]+'\n')

def send_get_request():
    result_label.config(text='GET request sent')
f=open('conf.ini', "w")
url = 'http://127.0.0.1:5000/'
server_path = 'server_holder.py'
cfg_file_path='config/data/cfg.txt'
done_work=[]
last_date=read_info(cfg_file_path)[0]
current_date=check_date()

def send_log():
	pass
root = tk.Tk()
root.title("Server Control App")

#start_button = tk.Button(root, text="Включить сервер", command=start_server)
send_post_button = tk.Button(root, text="Отправить POST запрос", command=send_post_request)
send_log = tk.Button(root, text="Сообщить об ошибке", command=send_log)


brand_name_entry = tk.Entry(root, width=30)
brand_name_entry.insert(0, "Brand Name")

frag_name_entry = tk.Entry(root, width=30)
frag_name_entry.insert(0, "Frag Name")

conc_entry = tk.Entry(root, width=30)
conc_entry.insert(0, "Conc")

ml_entry = tk.Entry(root, width=30)
ml_entry.insert(0, "ML")

result_label = tk.Label(root, text="")
number_label = tk.Label(root, text="0")
if current_date==last_date:
	file_name=datetime.now().date()
	
	current_datetime = datetime.now()
	date_string = current_datetime.strftime("%d-%m-%Y")
	file_name=date_string+'summary'+'.txt'
	file_path='config/data/'+file_name
	print('Продолжение сессии')
	print('Файл:',file_name)
	done_work=read_info(file_path)
	number_label.config(text=str(len(done_work)))
	for i in range(len(done_work)):
		print(i+1,done_work[i])
	pass
if current_date!=last_date:
	file_name=datetime.now().date()
	current_datetime = datetime.now()
	date_string = current_datetime.strftime("%d-%m-%Y")
	file_name=date_string+'summary'+'.txt'
	file_path='config/data/'+file_name
	with open(file_path, "w") as file:
		pass  # Ничего не записываем, создаем пустой файл
	with open(cfg_file_path, "w") as file:
		file.write(date_string)
	print(file_name)
	print('Новая сессия')
	print('Файл:')
	pass
#start_button.grid(row=0, column=0, pady=5)
send_post_button.grid(row=1, column=0, pady=5)
send_log.grid(row=1, column=1, pady=5)
brand_name_entry.grid(row=2, column=0, columnspan=2, pady=5)
frag_name_entry.grid(row=3, column=0, columnspan=2, pady=5)
conc_entry.grid(row=4, column=0, columnspan=2, pady=5)
ml_entry.grid(row=5, column=0, columnspan=2, pady=5)
result_label.grid(row=6, column=0, columnspan=2)
number_label.grid(row=8, column=0, pady=5)

root.mainloop()
