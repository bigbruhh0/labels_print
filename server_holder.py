import asyncio
import websockets
from aiohttp import web
import subprocess
import json
from functions import read_info,correct_line,read_info,do_corrections
from win32com.shell import shell, shellcon
user_path = shell.SHGetKnownFolderPath(shellcon.FOLDERID_Profile)
doc_path = shell.SHGetKnownFolderPath(shellcon.FOLDERID_Documents)
user_name='User'
buf_list=read_info(user_path+'/YandexDisk/ЭТИКЕТКИ/Для авт. печати/список замен.txt')
delete_list=read_info(user_path+'/YandexDisk/ЭТИКЕТКИ/Для авт. печати/список исключений(удаление).txt')
buf2=read_info(user_path+'/YandexDisk/ЭТИКЕТКИ/Для авт. печати/замены для концентрации.txt')
conc_replace_list=[]
for i in buf2:
	print(i)
	conc_replace_list.append(i.split('|_|'))

replace_list=[]
for i in buf_list:
	ba=i.split('|_|')
	replace_list.append(ba)
	

	
# Переменная, которую будем отслеживать
a = None
ws_data=[0,[]]
DRAW_SHOP=1
glob_DX=read_info('app_folder/config/data/cfg.txt')[1]
glob_DY=read_info('app_folder/config/data/cfg.txt')[2]
print(glob_DX,glob_DY)
# Обработчик POST-запросов для обновления переменной a
async def delete_pos(request):
    data = await request.json()  # Получаем данные запроса в формате JSON
    bup = json.loads(data.get('k'))  # Получаем значение по ключу 'k' из JSON
    print('Запрошено удаление:', bup)

    # Проверяем, содержится ли значение в списке ws_data[1]
    print(bup,ws_data[1],bup in ws_data[1])
    if bup in ws_data[1]:
        ws_data[1].remove(bup)  # Удаляем значение из списка
        ws_data[0] -= 1  # Уменьшаем значение ws_data[0] на 1
    print(ws_data)

    print('Удаление выполнено успешно')
    return web.Response(text="ok")
async def checkbutton(request):
	data = await request.json()  # Получаем данные запроса в формате JSON
	bup = json.loads(data.get('k'))  # Получаем значение по ключу 'k' из JSON
	print(bup)
	global DRAW_SHOP
	if bup[0]:
		DRAW_SHOP=0
	else:
		DRAW_SHOP=1
	print(DRAW_SHOP)
	return web.Response(text="ok")
async def check_axis(request):
	data = await request.json()  # Получаем данные запроса в формате JSON
	bup = json.loads(data.get('k'))  # Получаем значение по ключу 'k' из JSON
	print(bup)
	subprocess.run(['python', 'debug_axis.pyw']+bup, check=True)
	return web.Response(text= "ok")
async def set_ds(request):
	data = await request.json()  # Получаем данные запроса в формате JSON
	global glob_DX
	global glob_DY
	bup = json.loads(data.get('k'))  # Получаем значение по ключу 'k' из JSON
	print(bup['dx'],bup['dy'])
	aa=bup['dx']
	bb=bup['dy']
	glob_DX=aa
	glob_DY=bb
	return web.Response(text= "ok")
		
async def post_set_comp3(request):
	data = await request.json()
	print(data)
	if 'type' in data:
		_type=data.get('type')
		set_name='FUCKING SET NAME'
		lines_data = [
					["Jose Eisenberg", "Ambre D'Orient Secret V", "edp"],
					["Jose Eisenberg", "Ambre Nuit", "edp"],
					["Jose Eisenberg", "Grand Soir", "parf"],
					["Jose Eisenberg", "Just Before", "edt"],
					["Jose Eisenberg", "Amber Oud Gold Edition", "edp"],
					["Jose Eisenberg", "Amasadadbre D'Orient Secret V", "edp"],
					["Jose Eisenberg", "Ambre Nusdasdit", "edp"],
					["Jose Eisenberg", "Graasdsadnd Soir", "parf"],
					["Jose Eisenberg", "Just saaa", "edt"],
					["Jose Eisenberg", "Amber Oud Godsdasld Edition", "edp"],
		
		
				]
		args=[set_name]
		for i in lines_data:
			for j in i:
				args.append(j)
		#print(args,1)
		subprocess.run(['python', 'PDF_SET.pyw']+args, check=True)
		ws_data[0]+=len(lines_data)
		ws_data[1]=[set_name]
		return web.Response(text=_type + "ok")
async def update_variable(request):
	global count_do
	data = await request.post()
	print(request.query)
	b=request.query.get('brand')
	conv_data=request.query
	print(request.url,'CONVCONVONCONCOC')
	#return web.Response(text=data, status=400)
	#print(data['data'])
	if 'type' in conv_data:
		#print('val')
		_type = conv_data.get('type')
		if _type=='1':
			print('Создание этикетки обычной')
		elif _type=='2':
			print('Создание этикети сета')
		if _type == '1':
			brand_name = conv_data.get('brand')
			frag = conv_data.get('frag_name')
			frag_name = frag.upper()
			conc = conv_data.get('conc')
			ml = conv_data.get('ml')
			print('|'+brand_name+'|'+frag_name+'|'+conc+'|'+ml+'|')
			print([brand_name, frag_name, conc, ml])
			brand_name,frag_name,conc,ml=do_corrections(brand_name,frag_name,conc,ml,conc_replace_list,delete_list,buf_list,replace_list)
			if None in [brand_name, frag_name, conc, ml]:
				print("Одно из значений не было получено.")
				return "Не все данные предоставлены", 400
			#print(brand_name,frag_name,conc,ml)
			subprocess.run(['python', 'PDF_LABEL.pyw', brand_name, frag_name, conc, ml,str(DRAW_SHOP),glob_DX,glob_DY], check=True)
			#print(brand_name, frag_name, conc, ml)
			
			ws_data[0]+=1
			ws_data[1].append([brand_name,frag_name,conc,ml,str(request.url)])
			return web.Response(text=_type + "ok")
		elif _type=='2':
			set_name=conv_data.get('set_name')
			set_url=conv_data.get('set_url')
			set_ml=conv_data.get('ml')
			set_ml=set_ml.split('по')[1].replace(' ','')
			print('ML','|'+set_ml+'|')
			#получить и обработать информацию о ароматах в сете----------------------------
			lines_data = [
					["Jose Eisenberg", "Ambre D'Orient Secret V", "edp"],
					["Jose Eisenberg", "Ambre Nuit", "edp"],
					["Jose Eisenberg", "Grand Soir", "parf"],
					["Jose Eisenberg", "Just Before", "edt"],
					["Jose Eisenberg", "Amber Oud Gold Edition", "edp"],
					["Jose Eisenberg", "Amasadadbre D'Orient Secret V", "edp"],
					["Jose Eisenberg", "Ambre Nusdasdit", "edp"],
					["Jose Eisenberg", "Graasdsadnd Soir", "parf"],
					["Jose Eisenberg", "Just saaa", "edt"],
					["Jose Eisenberg", "Amber Oud Godsdasld Edition", "edp"],
			
			
					]
			#------------------------------------------------------------------------------
			args=[set_name]
			for i in lines_data:
				brand_name, frag_name, conc=i
				for j in i:
					args.append(j)
				#subprocess.run(['python', 'PDF_LABEL.pyw', brand_name, frag_name, conc, set_ml,str(DRAW_SHOP),glob_DX,glob_DY], check=True)
				ws_data[0]+=1
				ws_data[1].append([brand_name,frag_name,conc,set_ml])
			#print(args,1)
			subprocess.run(['python', 'PDF_SET.pyw']+args, check=True)
			return web.Response(text=_type + "ok")
		else:
			return web.Response(text="Value not provided in request", status=400)

# Эндпоинт для получения текущего значения переменной a
async def get_value(request):
    global a
    return web.Response(text=str(a))

# WebSocket обработчик для отправки значения переменной a клиенту
async def handle_ws(websocket, path):
    global ws_data
    while True:
        await websocket.send(json.dumps(ws_data))
        await asyncio.sleep(1)

# Главная функция сервера
async def main():
    app = web.Application()
    app.add_routes([web.post('/', update_variable),
					web.post('/set3/', post_set_comp3),
					web.get('/get_value', get_value),
					web.post('/del/', delete_pos),
					web.post('/check/', checkbutton),
					web.post('/axis/',check_axis),
					web.post('/set_ds/',set_ds)])
    app_runner = web.AppRunner(app)
    await app_runner.setup()
    server = web.TCPSite(app_runner, "localhost", 5000)#только для 3 компа, поменять на локалхост для остальных
    await server.start()

    async with websockets.serve(handle_ws, "localhost", 5001):
        print("WebSocket server started...")
        await asyncio.Future()  # Бесконечное ожидание

asyncio.run(main())
