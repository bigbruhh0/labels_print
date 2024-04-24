import requests

def send_post_request(url, data):
	try:
		response = requests.post(url, data=data)
		print("Статус код:", response.status_code)
		print("Ответ сервера:", response.text)
	except requests.exceptions.RequestException as e:
		print("Ошибка при отправке POST-запроса:", e)
lines=[]
with open('test_data.txt', 'r', encoding='utf-8') as file:
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
		cnt+=1
		a={}
print(data_set)
# URL вашего локального сервера
url = 'http://127.0.0.1:5000/'

# Данные, которые вы хотите отправить
for i in data_set:
	send_post_request(url, i)
