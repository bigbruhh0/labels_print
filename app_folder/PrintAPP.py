import subprocess
import requests
import tkinter as tk
from datetime import datetime
import threading
import asyncio
import websockets
import json
ws_get=[0,[]]
def check_date():
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%d-%m-%Y")
    print("Текущая дата:", current_date)
    day = current_datetime.day
    return current_date

def read_info(f_path):
    with open(f_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    kek = []
    for i in lines:
        p = i.find('|')
        kek.append(i)
    return kek
def send_post_del(ln):
	if len(ln)>0:
		data=json.dumps(ln)
		response = requests.post('http://localhost:5000/del', json={'k':data})
def send_post_request():
    _copy = 1
    brand_name = brand_name_entry.get()
    frag_name = frag_name_entry.get()
    conc = conc_entry.get()
    ml = ml_entry.get()
    try:
        response = requests.post(url, json={'brand_name': brand_name.replace('№', 'NO '), 'frag_name': frag_name.replace('№', 'NO '), 'conc': conc, 'ml': ml, 'type': '1'})
        if response.status_code == 200:
            result_label.config(text='POST request sent')
           # add_work(brand_name.upper() + '_' + frag_name + '_' + conc + '_' + ml)
            #number_label.config(text=str(len(done_work)))
        else:
            result_label.config(text='Failed to send POST request: {}'.format(response.text))
    except requests.exceptions.RequestException as e:
        result_label.config(text='Failed to send POST request: {}'.format(str(e)))
def edit_pdf():
	pass#brand_
async def handle_messages():
	uri = "ws://localhost:5001"
	async with websockets.connect(uri) as websocket:
		try:
			while True:
				message = await websocket.recv()
				my_list = json.loads(message)
				print("Received message from server:", my_list)
				# Вставьте здесь код обработки полученного сообщения
				global ws_get
				ws_get=my_list
				if len(my_list[1])>0:
					add_work(my_list[1][0][0].upper() + '_' + my_list[1][0][1] + '_' + my_list[1][0][2] + '_' + my_list[1][0][3])
					print(my_list[1])
					# Установка состояния полей ввода на normal
					brand_name_entry.config(state="normal")
					frag_name_entry.config(state="normal")
					conc_entry.config(state="normal")
					ml_entry.config(state="normal")

					# Вставка новых значений
					brand_name_entry.delete(0, tk.END)
					brand_name_entry.insert(0, my_list[1][0][0])
					frag_name_entry.delete(0, tk.END)
					frag_name_entry.insert(0, my_list[1][0][1])
					conc_entry.delete(0, tk.END)
					conc_entry.insert(0, my_list[1][0][2])
					ml_entry.delete(0, tk.END)
					ml_entry.insert(0, my_list[1][0][3])

					# Возврат состояния полей ввода в readonly
					brand_name_entry.config(state="readonly")
					frag_name_entry.config(state="readonly")
					conc_entry.config(state="readonly")
					ml_entry.config(state="readonly")
					number_label.config(text=str(len(done_work)))
					send_post_del(my_list[1][0])
					print('запрошено удаление',my_list[1])

		except websockets.exceptions.ConnectionClosed:
			print("Connection closed by server")

def add_work(text):
    global done_work
    current_datetime = datetime.now()
    hms = current_datetime.strftime("%H:%M:%S")
    text = hms + '|' + text.replace(' ', '_')
    print('ADD:', text)
    done_work.append(text)
    with open(file_path, "w") as file:
        for i in range(len(done_work)):
            file.write(done_work[i] + '\n')

def send_get_request():
    result_label.config(text='GET request sent')

f = open('conf.ini', "w")
url = 'http://127.0.0.1:5000/'
server_path = 'server_holder.py'
cfg_file_path = 'config/data/cfg.txt'
done_work = []
last_date = read_info(cfg_file_path)[0]
current_date = check_date()

def send_log():
    pass

root = tk.Tk()
root.title("Server Control App")

send_post_button = tk.Button(root, text="Открыть в редакторе", command=edit_pdf)
send_log = tk.Button(root, text="Сообщить об ошибке", command=send_log)

brand_name_entry = tk.Entry(root, width=30,state="readonly")
brand_name_entry.insert(0, "Brand Name")

frag_name_entry = tk.Entry(root, width=30,state="readonly")
frag_name_entry.insert(0, "Frag Name")

conc_entry = tk.Entry(root, width=30,state="readonly")
conc_entry.insert(0, "Conc")

ml_entry = tk.Entry(root, width=30,state="readonly")
ml_entry.insert(0, "ML")

result_label = tk.Label(root, text="")
number_label = tk.Label(root, text="0")

if current_date == last_date:
    file_name = datetime.now().date()
    current_datetime = datetime.now()
    date_string = current_datetime.strftime("%d-%m-%Y")
    file_name = date_string + 'summary' + '.txt'
    file_path = 'config/data/' + file_name
    print('Продолжение сессии')
    print('Файл:', file_name)
    done_work = read_info(file_path)
    number_label.config(text=str(len(done_work)))
    for i in range(len(done_work)):
        print(i + 1, done_work[i])
else:
    file_name = datetime.now().date()
    current_datetime = datetime.now()
    date_string = current_datetime.strftime("%d-%m-%Y")
    file_name = date_string + 'summary' + '.txt'
    file_path = 'config/data/' + file_name
    with open(file_path, "w") as file:
        pass  # Ничего не записываем, создаем пустой файл
    with open(cfg_file_path, "w") as file:
        file.write(date_string)
    print(file_name)
    print('Новая сессия')
    print('Файл:')
    
send_post_button.grid(row=1, column=0, pady=5)
send_log.grid(row=1, column=1, pady=5)
brand_name_entry.grid(row=2, column=0, columnspan=2, pady=5)
frag_name_entry.grid(row=3, column=0, columnspan=2, pady=5)
conc_entry.grid(row=4, column=0, columnspan=2, pady=5)
ml_entry.grid(row=5, column=0, columnspan=2, pady=5)
result_label.grid(row=6, column=0, columnspan=2)
number_label.place(relx=0.5, rely=.95, anchor="center")


# Функция для запуска асинхронной части (WebSocket)
def run_asyncio():
    asyncio.run(handle_messages())

# Запуск асинхронной части в отдельном потоке
asyncio_thread = threading.Thread(target=run_asyncio)
asyncio_thread.start()

root.mainloop()
