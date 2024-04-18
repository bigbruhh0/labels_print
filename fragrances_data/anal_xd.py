import openpyxl
 
workbook = openpyxl.load_workbook('data.xlsx')
sheet = workbook.active
data=[]
bad_data=[]
subs=[]
very_bad_data=[]
for row in sheet.iter_rows(values_only=True):
    data.append(row[1])
    #print(data[len(data)-1])
data=set(data)
mx=0
name=''
for i in data:
	ch=0
	cum=0
	buf=''
	if not i:
		pass
	else:
		for j in range(len(i)):
			if (ord(i[j])>=65 and ord(i[j])<=122)or(ord(i[j])>=30 and ord(i[j])<=39)or(ord(i[j])>=1040 and ord(i[j])<=1103):
				pass
			else:
				subs.append((i[j],ord(i[j])))
			if i[j]!=' ' and i[j]!='&' and j!=len(i)and i[j]!='-':
				cum+=1
				buf+=i[j]
			else:
				if cum>10:
					bad_data.append(buf)
				if cum>mx:
					mx=cum
					name=buf
				ch=1
				cum=0	
				buf=''
				
print(mx,name)
print(len(bad_data))
for i in bad_data:
	print (i)

for i in bad_data:
	for j in data:
		if i and j:
			if (i in j)and len(j)>40:
				very_bad_data.append(j)
print(len(very_bad_data))
for i in very_bad_data:
	print(i)
print('---------------------')
subs=set(subs)
print(subs)
