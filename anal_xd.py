with open('data/brand_names.txt', 'r') as file:
    lines = file.readlines()
struct_len=[]
for i in range(100):
	struct_len.append([])
for i in lines:
	l=len(i)
	struct_len[l].append(i)
for i in range(len(struct_len)):
	if len(struct_len[i])>0:
		print(i,len(struct_len[i]),struct_len[i][0])
