def split_line(l):
	flg_one=False
	flg_n=False
	syms_list=[" ",'!']
	cont_one=[]
	buf_d=''
	buf_const=''
	l1='/'
	l2='/'
	max_l=15
	for i in range(len(l)):
		if (l[i] in syms_list) or i==len(l)-1:
			g=len(buf_d)+len(buf_const)
			buf_d+=l[i]
			if g>11:
				if g<max_l:
					buf_const=buf_const+buf_d
					break
			else:
				buf_const=buf_const+buf_d
		
			buf_d=''
			
		else:
			buf_d+=l[i]
	l1=buf_const[:len(buf_const)-1]
	l2=l[len(l1)+1:]
	return l1,l2
def do_split(frag_name):
	s=[0,0,0]
	flg_one=False
	flg_n=False
	syms_list=[" ",'!']
	cont_one=[]
	cnt=0
	buf=''
	for i in range(len(frag_name)):
		if frag_name[i] in syms_list:
			if cnt>11 or i==len(frag_name)-1:
				if i==len(frag_name)-1:
					buf+=frag_name[i]
				if cnt>11:
					cont_one.append(buf)
				flg_one=True
			cnt=0
			buf=''
		else:
			buf+=frag_name[i]
			cnt+=1
			if i==len(frag_name)-1:
				if cnt>11: 
					cont_one.append(buf)
					flg_one=True
				cnt=0
				buf=''
				
	#print(cont_one)
	if flg_one:
		cnt_lines=0
		if len(cont_one)==1:
			s=[0,0,0,0]

			a=cont_one[0]
			b=frag_name.find(a)
			x_l=frag_name.find(a)
			x_r=x_l+len(a)-1
			if x_r==len(frag_name)-1:
				#print('/r/')
				cnt_lines=2
				s[3]=frag_name[x_l:x_r+1]
				s[2]=frag_name[:x_l-1]
				if len(s[2])>11:
					if len(s[2])>15:
						cnt_lines=3
						s[1],s[2]=split_line(s[2])
			elif x_l==0:
				#print('/l/')
				cnt_lines=2
				s[1]=frag_name[x_l:x_r+1]
				s[2]=frag_name[x_r+2:]
				if len(s[2])>11:
					cnt_lines=3
					s[2],s[3]=split_line(s[2])
			else:
				
				cnt_lines=3
				
				s[1]=frag_name[:x_l-1]
				s[2]=frag_name[x_l:x_r+1]
				s[3]=frag_name[x_r+2:]

	#s=[0,'MEMFIS','BOYS']		
	cnt_lines=2	
	return(s,cnt_lines)
def split_string(l):
	l=l.upper()
	except_list=[]
	with open('data/except_list.txt', 'r', encoding='utf-8') as file:
		for line in file:
			modified_line = line.replace('\n', '')
		
			except_list.append(modified_line)

	if l.find("NO.")>-1:
		l=l.replace("NO.","no.")
	
	buf=''
	buf_n=0
	syms_list=[" ",'!']
	line=['','']
	s=[0]
	if len(line)>10:
		line[0]=l
	else:
		for i in range(len(l)):
			if (l[i] in syms_list)or (i==len(l)-1):
				s.append(i)

		mid=len(l)/2
	
		min_D=9999999
		for i in range(len(s)):
			if i!=0 and i<len(s)-1:
				p1=s[i-1]
				p2=s[i]
				p3=s[i+1]
				if i>1:
					p1=s[i-1]+1
				if i==len(s)-2:
					p3=s[i+1]+1
				b1=l[p1:p2]
				b2=l[p2+1:p3]
				check_string=b1+' '+b2
				if check_string=="EAU DE":
					check_string+=l[s[i+1]:s[i+2]+1]
				
				for j in except_list:
					if check_string==j or check_string==j+' ' or check_string==' '+j:
						
						s[i]=150
						s[i+1]=150
				
		if len(s)>2 and len(l)>12:
			for i in range(len(s)):
				if abs(mid-s[i])<min_D:
					min_D=mid-s[i]
					buf=s[i]
					
			line[0]=l[:buf]
			line[1]=l[buf+1:]
		else:
			line[0]=l

	mx=0
	for i in line:
		if len(line)>mx:
			mx=len(line)
	print(line)
	return line
def get_info():
	brand='Les Liquides Imaginaires'
	name='DOM ROSA'
	conc='parf'
	ml='10'
	shop='АллюрПарфюм'
	return brand,name,conc,ml,shop
split_string("AKSDNJKASNFJKAS NJKSANFJKA 2KEKIS SHMEKIS")
