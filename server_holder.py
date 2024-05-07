import asyncio
import websockets
from aiohttp import web
import subprocess
import json
# Переменная, которую будем отслеживать
a = None
ws_data=[0,[]]
# Обработчик POST-запросов для обновления переменной a
async def delete_pos(request):
	data = await request.json()
	bup=json.loads(data.get('k'))
	print(bup)
	print('Запрошено удаление: ',bup)
	if bup in ws_data[1]:
		ws_data[1].remove(bup)
		ws_data[0]-=1
	print('Удаление выполнено успешно')
	return web.Response(text="ok")
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
			frag_name = frag
			conc = conv_data.get('conc')
			conc=conc.replace('(пробник)','')
			ml = conv_data.get('ml')
			print([brand_name, frag_name, conc, ml])

			if None in [brand_name, frag_name, conc, ml]:
				print("Одно из значений не было получено.")
				return "Не все данные предоставлены", 400
			#print(brand_name,frag_name,conc,ml)
			subprocess.run(['python', 'PDF_LABEL.pyw', brand_name, frag_name, conc, ml], check=True)
			#print(brand_name, frag_name, conc, ml)
			
			ws_data[0]+=1
			ws_data[1].append([brand_name,frag_name,conc,ml])
			return web.Response(text=_type + "ok")
		elif _type=='2':
			comp_3_url='http://192.168.0.103:5000/'
			send_post_request(comp_3_url,{'type':'2'})
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
                    web.get('/get_value', get_value)])
    app_runner = web.AppRunner(app)
    await app_runner.setup()
    server = web.TCPSite(app_runner, "localhost", 5000)#только для 3 компа, поменять на локалхост для остальных
    await server.start()

    async with websockets.serve(handle_ws, "localhost", 5001):
        print("WebSocket server started...")
        await asyncio.Future()  # Бесконечное ожидание

asyncio.run(main())
