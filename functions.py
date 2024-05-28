
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
def read_info(f_path):
    with open(f_path, "r", encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]
    kek = []
    for i in lines:
        p = i.find('|')
        kek.append(i)
    return kek
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
kekis={
	'No.': '№ ',
	
	'А' : '凡 ∀ ₳ Ǻ ǻ α ά Ά ẫ Ắ ắ Ằ ằ ẳ Ẵ ẵ Ä ª ä Å À Á Â å ã â à á Ã ᵰ',

	'B' : 'ℬ β ฿ ß Ђ Ɓ ƀ ხ 方'.split(' '),

	'C' : '☾ ℭ ℂ Ç ¢ ç Č ċ Ċ ĉ ς Ĉ ć Ć č Ḉ ḉ ⊂ ₡ ¢'.split(' '),

	'D' : 'Ɗ Ď ď Đ đ ð ∂ ₫ ȡ'.split(' '),

	'E' : 'ℯ £ Ē ℮ ē Ė ė Ę ě Ě ę Έ ê ξ Ê È € É ∑ Ế Ề Ể Ễ é è ع Є є έ ε'.split(' '),

	'F' : 'ℱ ₣ ƒ ∮ Ḟ ḟ ჶ ᶂ φ'.split(' '),

	'G' : 'ℊ Ǥ ǥ Ĝ ĝ Ğ ğ Ġ ġ Ģ ģ פ ᶃ ₲'.split(' '),

	'H' : 'ℍ ℋ ℎ ℌ ℏ Ĥ Ħ ħ Ή ♅ 廾 Ћ ђ Ḩ Һ ḩ♄'.split(' '),

	'I' : 'ℐ ℑ ί ι Ï Ί Î ì Ì í Í î ϊ ΐ Ĩ ĩ Ī ī Ĭ ĭ İ į Į'.split(' '),

	'J' : 'ჟ Ĵ ĵ ᶖ ɉ'.split(' '),

	'K' : '₭ Ќ k ќ ķ Ķ Ҝ ҝ ﻸ ᶄ'.split(' '),

	'L' : 'ℒ ℓ Ŀ ŀ £ Ĺ ĺ Ļ ļ λ ₤ Ł ł ľ Ľ Ḽ ḽ ȴ ￡'.split(' '),

	'M' : 'ℳ ʍ ᶆ Ḿ ḿ 爪 ₥'.split(' '),

	'N' : 'ℕ η ñ ח Ñ ή ŋ Ŋ Ń ń Ņ ņ Ň ň ŉ ȵ ℵ ₦'.split(' '),

	'O' : 'ℴ ტ ٥ Ό ó ό σ ǿ Ǿ Θ ò Ó Ò Ô ô Ö ö Õ õ ờ ớ ọ Ọ ợ Ợ ø Ø Ό Ở Ờ Ớ Ổ ổ Ợ Ō ō'.split(' '),

	'P' : 'ℙ ℘ þ Þ ρ 尸 Ҏ ҏ ᶈ ₱ ☧ ק ァ'.split(' '),

	'Q' : 'ℚ q Q ᶐ Ǭ ǭ ჹ'.split(' '),

	'R' : 'ℝ ℜ ℛ ℟ ჩ ř Ř ŗ Ŗ ŕ Ŕ ᶉ 尺'.split(' '),

	'S' : 'Ṧ ṧ ȿ ى § Ś ś š Š ş Ş ŝ Ŝ ₰ ∫ $ ֆ'.split(' '),

	'T' : '₸ † T t τ ΐ Ţ ţ Ť ť ŧ Ŧ ィ 干 Ṫ ṫ ナ テ ₮'.split(' '),

	'U' : '∪ Ũ ⋒ Ủ Ừ Ử Ữ Ự ύ ϋ Ù ú Ú ΰ ù Û û Ü ử ữ ự Џ ü ừ Ũ ũ Ū ū Ŭ ŭ ų Ų ű Ű ů Ů'.split(' '),

	'V' : '✔ ✓ ∨ √ Ṽ ṽ ᶌ ℣ ʋ'.split(' '),

	'W' : '₩ ẃ Ẃ ẁ Ẁ ẅ ώ ω ŵ Ŵ Ẅ ѡ'.split(' '),

	'X' : 'χ × ✗ ✘ ჯ Ẍ ẍ ᶍ ⏆'.split(' '),

	'Y' : 'ɣ Ẏ ẏ ϒ ɤ ￥ り'.split(' '),

	'Z' : 'ℤ ℨ ჳ 乙 Ẑ ẑ ɀ' .split(' '),
}

def correct_line(ln):
	buf=''
	for i in range(len(ln)):
		buf_i=ln[i]
		for j in kekis:
			for k in kekis[j]:
				b=k.replace(' ','')
				if b==ln[i]:
					if ln[i].islower():
						buf_i=j.lower()
					else:
						buf_i=j.upper()
		buf+=buf_i
	return(buf)
correct_line('Lanvin Oxygène Homme,')
def split_string(l,*tp):
	l=l.upper()
	except_list=[]
	if tp[0]==0:
		user_path=tp[1]
	else:
		user_path=tp[0]
	with open(user_path+'/YandexDisk/ЭТИКЕТКИ/Для авт. печати/список исключений(в одну строку).txt', 'r', encoding='utf-8') as file:
		for line in file:
			modified_line = line.replace('\n', '')
		
			except_list.append(modified_line)

	if l.find("NO.")>-1:
		pass#l=l.replace("NO.","no.")
	
	buf=''
	buf_n=0
	syms_list=[" "]
	line=['','']
	s=[0]
	if len(line)>10:
		line[0]=l
	else:
		for i in range(len(l)):
			if (l[i] in syms_list)or (i==len(l)-1):
				s.append(i)
		k=s
		print(s)
		for i in s:
			print('|'+l[i-3:i]+'|')
			if l[i-3:i]=='NO.' and l[i]==' ':
				s.remove(i)
		print(s)
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
		if tp:#############################CHECK IF PROBLEMS WITH SETS
			if tp[0]==0:
				k=22
			else:
				k=12
		if len(s)>2 and len(l)>k:
			for i in range(len(s)):
				if abs(mid-s[i])<min_D:
					min_D=mid-s[i]
					buf=s[i]
					
			line[0]=l[:buf]
			line[1]=l[buf+1:]
		else:
			line[0]=l

	mx=0
	linnne=[]
	for i in line:
		keks=i
		if i.find('NO.')>-1:
			print(i,1)
			if i[i.find('NO.')+3]==' ':
				keks=i[:i.find('NO.')+3]+i[i.find('NO.')+4:]
				print(i,2)
		if len(line)>mx:
			mx=len(line)
		linnne.append(keks)
	print(linnne)
	print('LINELNEIENE')
	return linnne
def get_info():
	brand='Les Liquides Imaginaires'
	name='DOM ROSA'
	conc='parf'
	ml='10'
	shop='АллюрПарфюм'
	return brand,name,conc,ml,shop
def add_image_to_pdf(image_path, pdf_path,y,c):
    image = Image.open(image_path)

    image_width, image_height = image.size

    pdf_width, pdf_height = (4.5*cm,4.7*cm)

    new_image_width = pdf_width

    new_image_height = 10

    c.drawImage(image_path, 0, y, width=new_image_width, height=new_image_height)
def create_text_image(text, image_path, font_size=20, font_path=None):
    image = Image.new("RGBA", (5048, 2024), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    draw.text((10, 10), text, fill="black", font=font)

    bbox = image.getbbox()

    cropped_image = image.crop(bbox)

    cropped_image.save(image_path)

def do_corrections(a,b,c,d,conc_replace_list,delete_list,buf_list,replace_list):
	aa=a
	bb=b
	cc=c
	dd=d
	for i in delete_list: #удаление
		print(i)
		bb=bb.replace(i.upper(),'')
		cc=cc.replace(i,'')
		print(bb,b,cc,c)

	for i in replace_list: # замены
		print('------------------------------------')
		print('|'+a+'|'+b+'|'+c+'|'+d+'|')
		print('|'+i[0]+'|'+i[1]+'|')
		if b.find(i[0].upper())>-1:
			bb=bb.replace(i[0],i[1]).upper()
		if a.find(i[0])>-1:
			print('12359798----------')
			aa=aa.replace(i[0],i[1])
		if c.find(i[0])>-1:
			cc=cc.replace(i[0],i[1])
	for i in conc_replace_list: # винтаж /старый и тп
		if b.find(i[0].upper())>-1:
			print('FOUND')
			cc=i[1]+', '+cc
	aa=correct_line(aa)
	bb=correct_line(bb)
	return aa,bb,cc,dd
