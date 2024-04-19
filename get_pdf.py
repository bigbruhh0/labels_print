from reportlab.lib.colors import red
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
import subprocess
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase.ttfonts import TTFont
from functions import do_split,split_line,get_info,split_string
import sys

import os

file_path = 'test_pdfs/test'+str(1)+'.pdf'
k=0
while(os.path.exists(file_path)):
	k+=1
	file_path = 'test_pdfs/test'+str(k)+'.pdf'

sh="Ornitons"
lg="steelfish"
sh1="OrnitonsBold"
sh2="Afrora"
	

pdfmetrics.registerFont(TTFont('long_font', 'fonts/'+lg+'.ttf'))
pdfmetrics.registerFont(TTFont('info_font', 'fonts/info_font.ttf'))
pdfmetrics.registerFont(TTFont('bold_font', 'fonts/bold_font.ttf'))
pdfmetrics.registerFont(TTFont('short_font', 'fonts/'+sh+'.ttf'))
pdfmetrics.registerFont(TTFont('short1_font', 'fonts/'+sh1+'.ttf'))

def get_height(font_list):
	string_height=0
	for i in font_list:
		face = pdfmetrics.getFont(i[0]).face
		string_height += (face.ascent - face.descent) / 1000 * i[1]
	return string_height
#addMapping('sh_n_font', 0, 0, 'shop_font.ttf')  # 'MyFont' - имя шрифта, 'myfont.ttf' - путь к файлу шрифта

shop_font=['info_font',8]
conc_font=['info_font',8]
frag_font=['short_font',11]
brand_font=['short_font',8]
my_style=ParagraphStyle('style1',
	fontName=shop_font[0],
	fontSize=shop_font[1],
	#backColor="#FFFF00",
	wordWrap = TA_JUSTIFY,
	alignment=TA_CENTER,
	borderPadding=0,
	leftIndent=0,
	rightIndent=0,
	spaceAfter=0,
	spaceBefore=0,
	splitLongWords=True,
	spaceShrinkage=0.05,
	#textTransform='uppercase'
	underlineWidth=0,
	underlineOffset=0,
	underlineGap=0,
	leading=6,
	)
	
brand_name=sys.argv[1]
frag_name=sys.argv[2]
conc=sys.argv[3]
ml=sys.argv[4]
shop_name="АллюрПарфюм"
width = 2.5 * cm
height = 1.8 * cm
s=split_string(frag_name)
print(s)
strings=[]
for i in s:
	if i!='':
		strings.append(i)
print(strings)
STR_MAX=''
max_len=0
for i in strings:
	if len(i)>max_len:
		max_len=len(i)
		STR_MAX=i
print(STR_MAX)

l_b=len(brand_name)
if l_b>17:
	brand_font='long_font'
elif l_b>17:
	brand_font='short_font'
else:
	brand_font='short1_font'

if max_len<=13:
	frag_font='short_font'
else:
	frag_font='long_font'
	

c = Canvas(file_path, pagesize=(width,height))
c.setLineWidth(0.1*cm)
#c.rect(0,0, width, height)



#BRAND LABEL
l_size=9
text_width=stringWidth(brand_name,brand_font,l_size)

#подгон по ширине
while(text_width>width-0.3*cm):
	
	l_size-=.1
	text_width=stringWidth(brand_name,brand_font,l_size)

print(l_size)
#########################################

#FRAGRANCE NAME

min_H=0.1*cm+shop_font[1]*0.8+shop_font[1]*0.8+2
max_H=height-l_size*.8-4
L_SIZE=20
L_COUNT=len(strings)
text_H=(L_SIZE*.8+1)*L_COUNT
print(max_H-min_H,'HHH')
#подгон по высоте первичный
while(text_H>max_H-min_H-2):
	L_SIZE-=.1
	#text_width=stringWidth(txt,frag_font,L_SIZE)
	text_H=(L_SIZE*.8)*L_COUNT
str_sizes=[0,0,0]
str_y=[0,0,0]
print("FRAG SIZE: ",L_SIZE)
yy=0
#подгон по ширине
for i in range(len(strings)):
	str_sizes[i]=L_SIZE
	text_width=stringWidth(strings[i],frag_font,str_sizes[i])
	while (text_width>width-0.1*cm):
		str_sizes[i]-=.1
		text_width=stringWidth(strings[i],frag_font,str_sizes[i])

text_h=0
text_H=0
print(str_sizes)
max_Len=0
#ПОДГОН ПО ВЫСОТЕ ВТОРИЧНЫЙ ИНДИВИДУАЛЬНЫЙ/ ВЫЯВЛЕНИЕ d
while(text_H<max_H-min_H ):
	for i in range(len(str_sizes)):
		d=1
		if str_sizes[i]>0:
			if len(strings[i])<max_len:
				text_H=d
				bf=str_sizes[i]
				str_sizes[i]+=.1
				#max_Len=stringWidth(strings[i],frag_font,str_sizes[i])<width-0.1*cm
				for j in range(len(str_sizes)):
						text_H+=str_sizes[j]*.8+d
	if len(strings)==1:
		#text_H+=str_sizes[i]*.8+d
		break
	if len(strings)==2:
		if len(strings[0])==len(strings[1]):
			#text_H+=str_sizes[i]*.8+d+str_sizes[i]*.8+d
			break
	print(str_sizes)
for i in range(len(strings)):
	if len(strings[i])<max_len:
		while(stringWidth(strings[i],frag_font,str_sizes[i])>width-0.1*cm):
			str_sizes[i]-=.1
min_L=90

for j in range(len(strings)):
	i=len(strings)-j-1
	if str_sizes[i]>0 and str_sizes[i]<min_L:
		min_L=str_sizes[i]
	str_y[i]=yy
	yy+=(str_sizes[i]*.8)
	
	print(yy)			
			##trash
d=0
#ВЫЯВЛЕНИЕ d	
diff=1	
def find_d():	
	d=((height-2)-text_H)/(len(strings)+5)
	print(d,d,d,d,d)
	return d

#l_size=min_L-2
max_H=height-l_size*.8-4



if len(strings)==1:
	text_H=str_sizes[0]*.8
else:
	text_H=str_sizes[0]*.8+str_sizes[1]*.8
text_H=text_H+l_size*0.8+shop_font[1]*0.8*2
d=0
d=find_d()


c.setLineWidth(.1)
print('MAXH:',max_H,';h:',max_H-min_H,';text_H:',text_H,'d:',d,';',len(strings))
#c.rect(5,min_H,min_H,text_H)

min_H=d*3+shop_font[1]*0.75+shop_font[1]*0.7

for j in range(len(strings)):
	
	i=len(strings)-j-1
	c.setFont(frag_font, str_sizes[i])  # Задаем шрифт и размер
	text_width=stringWidth(strings[i],frag_font,str_sizes[i])
	c.rect(width/2-text_width/2,min_H+str_y[i]+(d+1)*(j)+diff,stringWidth(strings[i],frag_font,str_sizes[i]),str_sizes[i]*0.8)
	stir=c.drawString(width/2-text_width/2,min_H+str_y[i]+(d+1)*(j)+diff,strings[i])#Рисуем название
	print(d)
	print(str_y[i],"string_",i)


dd=height-max_H-l_size*.8
c.setFont(brand_font, l_size)  # Рисуем бренд
name_H=0

for i in str_sizes:
	if i>0:
		name_H+=(i+d)*0.8
c.rect(width/2-stringWidth(brand_name,brand_font,l_size)/2,name_H+min_H+d+diff,stringWidth(brand_name,brand_font,l_size),l_size*0.8)
brand_BOX=c.drawString(width/2-stringWidth(brand_name,brand_font,l_size)/2,name_H+min_H+d+diff,brand_name)
#SHOP NAME
c.setFont(shop_font[0], shop_font[1])
c.rect(width/2-stringWidth(shop_name,shop_font[0],shop_font[1])/2,d+diff,stringWidth(shop_name,shop_font[0],shop_font[1]),shop_font[1]*0.7)
shop_BOX=c.drawString(width/2-stringWidth(shop_name,shop_font[0],shop_font[1])/2,d+diff,shop_name)
min_L=0.1*cm+shop_font[1]*0.8+shop_font[1]*0.8
#CONCENTRATION
c.setFont(shop_font[0], shop_font[1])
c.rect(width/2-stringWidth("{0} {1} ml".format(conc,ml),shop_font[0],shop_font[1])/2,shop_font[1]*0.75+d*2+diff,stringWidth("{0} {1} ml".format(conc,ml),shop_font[0],shop_font[1]),shop_font[1]*0.6)
conc_BOX=c.drawString(width/2-stringWidth("{0} {1} ml".format(conc,ml),shop_font[0],shop_font[1])/2,shop_font[1]*0.75+d*2+diff,"{0} {1} ml".format(conc,ml))
f = open('test_pdfs/test'+str(k)+'.txt', "w")
f.writelines([sh,' / ',lg,' / ',sh1,' / ',sh2,' / ',frag_font,' / ',brand_font])
f.close()
c.save()
# Open the generated PDF using default PDF viewer
#subprocess.Popen(["start", "", file_path], shell=True)
print(height-max_H-l_size*.8,0,0,0,0)
