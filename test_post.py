import asyncio
import websockets
from aiohttp import web
import subprocess
import json
import requests
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
set_id=read_info('handle_set_id.txt')[0]
replace_list=[]
for i in buf_list:
	ba=i.split('|_|')
	replace_list.append(ba)
	
a = None
DRAW_SHOP=1
glob_DX=read_info('app_folder/config/data/cfg.txt')[1]
glob_DY=read_info('app_folder/config/data/cfg.txt')[2]

a=requests.get('https://allureparfum.ru/rest/1/56a3dyn1xzwl8ado/retailcrm.get_product/?id='+set_id).json()
print(a["result"]["response"])
print(a["result"]["response"]["SET"])
set_name=a["result"]["response"]["BRAND"]+' '+a["result"]["response"]["NAME"]
lines_data=[]
ML=0
for i in a["result"]["response"]["SET"]:
	a=i["BRAND"]
	b=i["NAME"]
	c=i["SKU_TYPE"]
	ML=i["VOLUME"]
	#print(a,b,c,ML)
	a,b,c,d=do_corrections(a,b,c,ML,conc_replace_list,delete_list,buf_list,replace_list)
	lines_data.append([a,b,c])
args=[set_name]
lines_data.sort()
print(lines_data)
for i in lines_data:
	for j in i:
		args.append(j)
print(args)

subprocess.run(['python', 'PDF_SET.pyw']+args, check=True)
print(args)
for i in lines_data:
	pass#subprocess.run(['python', 'PDF_LABEL.pyw', i[0], i[1], i[2], ML,str(DRAW_SHOP),glob_DX,glob_DY], check=True)
'''def send_post_request(url, data):
	try:
		response = requests.post(url, json=data)
		print("Статус код:", response.status_code)
		print("Ответ сервера:", response.text)
	except requests.exceptions.RequestException as e:
		print("Ошибка при отправке POST-запроса:", e)
lines=[]
with open('data/test_data.txt', 'r', encoding='utf-8') as file:
    for line in file:
        modified_line = line.replace('№', 'No ')
        print(modified_line)
        lines.append(modified_line)
		
cnt=0
data_set=[]
a={}
for i in range(len(lines)):
	b=(i+1)-cnt*4
	if b==1:
		a['type']='1'
		a['brand_name']=lines[i].replace('\n','')
	if b==2:
		a['frag_name']=lines[i].replace('\n','')
	if b==3:
		a['conc']=lines[i].replace('\n','')
	if b==4:
		a['ml']=lines[i].replace('\n','')

	print(a)
	if (i+1)%4==0:
		data_set.append(a)
		print('a',a)
		cnt+=1
		a={}
print(data_set)
# URL вашего локального сервера
url = 'http://localhost:5000/'

# Данные, которые вы хотите отправить
for i in data_set:
	print(i)
	#send_post_request(url,i)
comp_3_url='http://192.168.0.111:5000/'
send_post_request(url,{'type':'2'})'''
