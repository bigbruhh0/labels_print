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

pdfmetrics.registerFont(TTFont('long_font', 'fonts/FOR_LONG_NAMES.ttf'))
pdfmetrics.registerFont(TTFont('info_font', 'fonts/info_font.ttf'))
pdfmetrics.registerFont(TTFont('bold_font', 'fonts/bold_font.ttf'))
pdfmetrics.registerFont(TTFont('short_font', 'fonts/FOR_SHORT_NAMES.ttf'))

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

if len(brand_name)>11:
	brand_font='long_font'
else:
	brand_font='short_font'

if max_len<=7 and len(strings)==1:
	frag_font='short_font'
elif max_len<=10 and len(strings)==2:
	frag_font='short_font'
else:
	frag_font='long_font'
	
	
c = Canvas("test.pdf", pagesize=(width,height))
c.setLineWidth(0.1*cm)
#c.rect(0,0, width, height)
#SHOP NAME
p1 = Paragraph(shop_name,my_style)
p1.wrapOn(c, 2.5 * cm, 0.0 * cm)
p1.drawOn(c, 0.0 * cm, 0.2 * cm)

#CONCENTRATION
p2 = Paragraph(conc+' '+ml+' ml',my_style)
p2.wrapOn(c, 2.5 * cm, 0.0 * cm)
p2.drawOn(c, 0.0 * cm, 0.25 * cm+get_height([shop_font])*.65)


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

min_H=18
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

#ПОДГОН ПО ВЫСОТЕ ВТОРИЧНЫЙ ИНДИВИДУАЛЬНЫЙ/ ВЫЯВЛЕНИЕ d
while(text_H<max_H-min_H):
	for i in range(len(str_sizes)):
		d=1
		if str_sizes[i]>0:
			if len(strings[i])<max_len:
				text_H=d
				bf=str_sizes[i]
				str_sizes[i]+=.1
				for j in range(len(str_sizes)):
					text_H+=str_sizes[j]*.8+d
	if len(strings)==1:
		break
	print(str_sizes)
min_L=90

for j in range(len(strings)):
	i=len(strings)-j-1
	if str_sizes[i]>0 and str_sizes[i]<min_L:
		min_L=str_sizes[i]
	str_y[i]=yy
	yy+=(str_sizes[i]*.8)
	
	print(yy)			
			
d=0
#ВЫЯВЛЕНИЕ d		
def find_d():	
	if len(strings)>1:	
		d=max_H-min_H-text_H
		d=abs(d/((len(strings)+1)))/2
	else:
		d=max_H-2-min_H-len(strings)*L_SIZE*.8
		d=abs(d/((len(strings)+1)/2))

#l_size=min_L-2
max_H=height-l_size*.8-4

c.setFont(brand_font, l_size)  # Рисуем бренд
stir=c.drawString(width/2-stringWidth(brand_name,brand_font,l_size)/2,height-l_size*.8-4,brand_name)

find_d()
print('MAXH:',max_H,';h:',max_H-min_H,';text_H:',text_H,'d:',d,';')

for j in range(len(strings)):
	i=len(strings)-j-1
	c.setFont(frag_font, str_sizes[i])  # Задаем шрифт и размер
	text_width=stringWidth(strings[i],frag_font,str_sizes[i])
	stir=c.drawString(width/2-text_width/2,min_H+str_y[i]+(d+1)*j,strings[i])#Рисуем название
	print(str_y[i],"string_",i)
c.setLineWidth(1)
p1.fontSize=6
c.line(0,min_H,0,max_H)
	
c.save()
print(width,height,2.5*cm,1.8*cm,cm)
# Open the generated PDF using default PDF viewer
subprocess.Popen(["start", "", "test.pdf"], shell=True)
