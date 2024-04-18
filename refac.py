flg_one=False
flg_n=False

syms_list=[" ",'!']
cont_one=[]
def split_line(l):
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
				
	print(cont_one)
	if flg_one:
		cnt_lines=0
		if len(cont_one)==1:
			s=[0,0,0,0]

			a=cont_one[0]
			b=frag_name.find(a)
			x_l=frag_name.find(a)
			x_r=x_l+len(a)-1
			if x_r==len(frag_name)-1:
				print('/r/')
				cnt_lines=2
				s[3]=frag_name[x_l:x_r+1]
				s[2]=frag_name[:x_l-1]
				if len(s[2])>11:
					if len(s[2])>15:
						cnt_lines=3
						s[1],s[2]=split_line(s[2])
			elif x_l==0:
				print('/l/')
				cnt_lines=2
				s[1]=frag_name[x_l:x_r+1]
				s[2]=frag_name[x_r+2:]
				if len(s[2])>11:
					cnt_lines=3
					s[2],s[3]=split_line(s[2])
			else:
				print('/m/')
				cnt_lines=3
				
				s[1]=frag_name[:x_l-1]
				s[2]=frag_name[x_l:x_r+1]
				s[3]=frag_name[x_r+2:]
	print(s)			
	return(s)
	
	
do_split("VIVA LA MEGA EDITION BESHKERMEKISTAN")
