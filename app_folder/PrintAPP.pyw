import subprocess
import requests
import tkinter as tk
from datetime import datetime
import threading
import asyncio
import websockets
import json
from tkinter import ttk
ws_get=[0,[]]
def check_date():
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%d-%m-%Y")
    print("Текущая дата:", current_date)
    day = current_datetime.day
    return current_date
def set_ds():
	url = 'http://localhost:5000/set_ds/'  # URL для отправки запроса
	a=x_entry.get()
	b=y_entry.get()
	lil=[str(a),str(b)]
	data = {'k': json.dumps({'dx':str(a),'dy':str(b)})}  # Преобразуем список в JSON и передаем как параметр запроса

	try:
		response = requests.post(url, json=data)  # Отправляем POST-запрос с JSON-данными
		response.raise_for_status()  # Проверяем, есть ли ошибки в ответе
		print("Запрос успешно отправлен")
	except requests.exceptions.RequestException as e:
		print("Ошибка при отправке запроса:", e)
def test_x():
	url = 'http://localhost:5000/axis/'  # URL для отправки запроса
	data = {'k': json.dumps(['x'])}  # Преобразуем список в JSON и передаем как параметр запроса

	try:
		response = requests.post(url, json=data)  # Отправляем POST-запрос с JSON-данными
		response.raise_for_status()  # Проверяем, есть ли ошибки в ответе
		print("Запрос успешно отправлен")
	except requests.exceptions.RequestException as e:
		print("Ошибка при отправке запроса:", e)
def test_y():
	url = 'http://localhost:5000/axis/'  # URL для отправки запроса
	data = {'k': json.dumps(['y'])}  # Преобразуем список в JSON и передаем как параметр запроса

	try:
		response = requests.post(url, json=data)  # Отправляем POST-запрос с JSON-данными
		response.raise_for_status()  # Проверяем, есть ли ошибки в ответе
		print("Запрос успешно отправлен")
	except requests.exceptions.RequestException as e:
		print("Ошибка при отправке запроса:", e)

def read_info(f_path):
    with open(f_path, "r") as file:
        lines = [line.strip() for line in file.readlines()]
    kek = []
    for i in lines:
        p = i.find('|')
        kek.append(i)
    return kek
def send_post_del(ln):
    url = 'http://localhost:5000/del/'  # URL для отправки запроса
    data = {'k': json.dumps(ln)}  # Преобразуем список в JSON и передаем как параметр запроса

    try:
        response = requests.post(url, json=data)  # Отправляем POST-запрос с JSON-данными
        response.raise_for_status()  # Проверяем, есть ли ошибки в ответе
        print("Запрос успешно отправлен")
    except requests.exceptions.RequestException as e:
        print("Ошибка при отправке запроса:", e)
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
				#print("Received message from server:", my_list)
				# Вставьте здесь код обработки полученного сообщения
				global ws_get
				ws_get=my_list
				if len(my_list[1])>0:
					add_work(my_list[1][0][0].upper() + '^' + my_list[1][0][1] + '^' + my_list[1][0][2] + '^' + my_list[1][0][3])
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



# Задание геометрии дочернего окна

def add_to_tree(item):
	time_data, product_data = item.split("|")
	a, b, c, d = product_data.split("^")
	done_work_listbox.insert('', tk.END, values=(len(done_work_listbox.get_children())+1,a, b, c, d))
	done_work_listbox.yview_moveto(1)
	
def append_to_file(filename, value):
	with open(filename, 'a') as file:
		current_datetime = datetime.now()
		hms = current_datetime.strftime("%d:%m:%y:%H:%M:%S")
		file.write(value.replace('\n','') +'|'+hms+'\n')


def add_work(text):
    global done_work
    current_datetime = datetime.now()
    hms = current_datetime.strftime("%H:%M:%S")
    text = hms + '|' + text
    print('ADD:', text)
    done_work.append(text)
    add_to_tree(text)
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
	a,b,c,d=brand_name_entry.get(),frag_name_entry.get(),conc_entry.get(),ml_entry.get()
	append_to_file('config/problem_labels.txt',a+b+c+d+'\n')

root = tk.Tk()
root.title("Server Control App")
button_frame = tk.Frame(root)
button_frame.pack()
d_axis=tk.Frame(button_frame)

x_set=tk.Frame(d_axis)
y_set=tk.Frame(d_axis)
x_set.pack(side=tk.LEFT)
y_set.pack(side=tk.RIGHT)
d_axis.pack()
send_post_button = tk.Button(button_frame, text="Открыть в редакторе", command=edit_pdf)
send_log = tk.Button(button_frame, text="Сообщить об ошибке", command=send_log)
ax_x = tk.Button(x_set, text="тест Х", command=test_x)
ax_y = tk.Button(y_set, text="тест Y", command=test_y)
confirm_ds = tk.Button(button_frame, text="Установить параметры", command=set_ds)
confirm_ds.pack(side=tk.BOTTOM)


brand_name_entry = tk.Entry(root, width=30,state="readonly")
brand_name_entry.insert(0, "Brand Name")

frag_name_entry = tk.Entry(root, width=30,state="readonly")
frag_name_entry.insert(0, "Frag Name")

conc_entry = tk.Entry(root, width=30,state="readonly")
conc_entry.insert(0, "Conc")

ml_entry = tk.Entry(root, width=30,state="readonly")
ml_entry.insert(0, "ML")

x_entry=tk.Entry(x_set, width=30)
y_entry=tk.Entry(y_set, width=30)



result_label = tk.Label(root, text="")
number_label = tk.Label(root, text="0")

#open_list_button = tk.Button(button_frame, text="Open List Window", command=lambda: create_list_window(done_work, root))
#open_list_button.pack(side=tk.LEFT,pady=20)

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
# Создание Listbox для отображения списка done_work
parent_geometry = root.geometry()
parent_x, parent_y = map(int, parent_geometry.split('+')[1:3])

# Размеры и позиция дочернего окна относительно родительского окна
child_width = 700
child_height = 200
child_x = parent_x + root.winfo_width()  # Позиция X окна (правый край родительского окна)
child_y = parent_y  # Позиция Y окна (верхняя граница родительского окна)

#list_window = tk.Toplevel(root)
#list_window.title("Done Work List")
#list_window.geometry(f"{child_width}x{child_height}+{child_x}+{child_y}")
done_work_listbox = ttk.Treeview(root, columns=('d','A', 'B', 'C', 'D'), show='headings')
done_work_listbox.heading('d', text='#')
done_work_listbox.heading('A', text='Бренд')
done_work_listbox.heading('B', text='Аромат')
done_work_listbox.heading('C', text='Конц.')
done_work_listbox.heading('D', text='Объем')
done_work_listbox.column('d', width=30, anchor="center")
done_work_listbox.column('C', width=30, anchor="center")
done_work_listbox.column('D', width=30, anchor="center")
done_work_listbox.column('A', width=250, anchor="center")
done_work_listbox.column('B', width=300, anchor="center")
for i in done_work:
	add_to_tree(i)
# Размещение Listbox на окне
def check_action():
	url = 'http://localhost:5000/check/'  # URL для отправки запроса
	
	data = {'k': json.dumps([checkvar.get()])}  # Преобразуем список в JSON и передаем как параметр запроса

	try:
		response = requests.post(url, json=data)  # Отправляем POST-запрос с JSON-данными
		response.raise_for_status()  # Проверяем, есть ли ошибки в ответе
		print("Запрос успешно отправлен")
	except requests.exceptions.RequestException as e:
		print("Ошибка при отправке запроса:", e)
checkvar = tk.BooleanVar()
check_button = tk.Checkbutton(root, text="НЕ ПЕЧАТАТЬ НАЗВАНИЕ МАГАЗИНА", variable=checkvar,command=check_action)
check_button.pack(side=tk.TOP)
done_work_listbox.pack(padx=10, pady=10)
send_post_button.pack(side=tk.LEFT, pady=5)
send_log.pack(side=tk.LEFT, pady=5)
ax_x.pack(side=tk.TOP, pady=5)
ax_y.pack(side=tk.TOP, pady=5)

brand_name_entry.pack(side=tk.TOP, pady=5)
frag_name_entry.pack(side=tk.TOP, pady=5)
conc_entry.pack(side=tk.TOP, pady=5)
ml_entry.pack(side=tk.TOP, pady=5)
result_label.pack(side=tk.TOP)
number_label.pack(side=tk.BOTTOM)
y_entry.pack(side=tk.BOTTOM)
x_entry.pack(side=tk.BOTTOM)




def on_item_select(event):
	# Получить индекс выбранной строки
	selected_row = done_work_listbox.selection()[0]

	# Получить данные из выбранной строки
	data = done_work_listbox.item(selected_row)['values']
	brand_name_entry.config(state="normal")
	frag_name_entry.config(state="normal")
	conc_entry.config(state="normal")
	ml_entry.config(state="normal")
	# Вставить данные в Entry
	brand_name_entry.delete(0, tk.END)  # Очистить Entry перед вставкой новых данных
	brand_name_entry.insert(0, data[1])  # Пример: вставить первый элемент из строки таблицы
	frag_name_entry.delete(0, tk.END)  # Очистить Entry перед вставкой новых данных
	frag_name_entry.insert(0, data[2])  # Пример: вставить первый элемент из строки таблицы
	conc_entry.delete(0, tk.END)  # Очистить Entry перед вставкой новых данных
	conc_entry.insert(0, data[3])  # Пример: вставить первый элемент из строки таблицы
	ml_entry.delete(0, tk.END)  # Очистить Entry перед вставкой новых данных
	ml_entry.insert(0, data[4])  # Пример: вставить первый элемент из строки таблицы
	brand_name_entry.config(state="readonly")
	frag_name_entry.config(state="readonly")
	conc_entry.config(state="readonly")
	ml_entry.config(state="readonly")

# Привязать обработчик событий к таблице
done_work_listbox.bind('<ButtonRelease-1>', on_item_select)

# Функция для запуска асинхронной части (WebSocket)
def run_asyncio():
    asyncio.run(handle_messages())

# Запуск асинхронной части в отдельном потоке
asyncio_thread = threading.Thread(target=run_asyncio)
asyncio_thread.start()



root.mainloop()
