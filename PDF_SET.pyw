from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import red
from reportlab.lib import colors
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from functions import do_split, split_line, get_info, split_string#,add_image_to_pdf,create_text_image
from pathlib import Path
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageFilter
from reportlab.lib.units import cm
from win32com.shell import shell, shellcon
import sys
import os
user_path = shell.SHGetKnownFolderPath(shellcon.FOLDERID_Profile)
doc_path = shell.SHGetKnownFolderPath(shellcon.FOLDERID_Documents)
user_name='User Trade'
def add_image_to_pdf(image_path, pdf_path,y,c):
    image = Image.open(image_path)

    image_width, image_height = image.size

    pdf_width, pdf_height = (4.5*cm,4.7*cm)

    new_image_width = pdf_width

    new_image_height = 10

    c.drawImage(image_path, 0, y, width=new_image_width, height=new_image_height)
def create_text_image(text, image_path, font_size=20, font_path=None):
	image = Image.new("RGBA", (10096, 10096), (255, 255, 255, 0))
	draw = ImageDraw.Draw(image)

	if font_path:
		font = ImageFont.truetype(font_path, font_size)
	else:
		font = ImageFont.load_default()

	draw.text((10, 10), text, fill="black", font=font)

	bbox = image.getbbox()

	cropped_image = image.crop(bbox)

	cropped_image.save(image_path)

def rg(spis):
	return range(len(spis))
def getHto(pos):
	h=0
	for i in range(pos+1):
		h+=lines_obj[i].image_H
	return h
class _lines:
	def __init__(self,pos, brand_name, frag_name, conc):
		self.pos=pos
		self.brand_name = brand_name
		self.frag_name = frag_name
		self.fontName='list_font'
		self.conc = conc
		print(self.brand_name,self.frag_name,self.conc)
		self.text=self.brand_name+' - '+self.frag_name+', '+self.conc
		img_path=user_path+'/YandexDisk/ЭТИКЕТКИ/Для авт. печати/set_cache(не трогать)/'
		img_path=img_path+self.brand_name+' - '+self.frag_name+', '+self.conc+'.png'
		self.img_path=img_path
		if os.path.exists(img_path):
			pass
		else:
			create_text_image(self.brand_name+' - '+self.frag_name+', '+self.conc,img_path,font_size, font_path)
		self.fontSize=12
		self.k=0.7
		self.x=x_border
		self.y=H
		self.image = Image.open(img_path)
	def drawSelf(self,d,last_shift):
		new_image_width = self.orig_w*self.k
		new_image_height = self.image_H
		numb_size=self.image_H/1
		c.setFont('numb_font', numb_size)
		l_w=stringWidth(str(self.pos+1)+'.  ',self.fontName,numb_size)
		if self.pos==9:
			k1=stringWidth('1 ',self.fontName,numb_size)
		else:
			k1=0
		c.drawString(x_border-k1,-last_shift/2+ name_obj.y-(d+self.image_H)*(self.pos+1)+self.image_H*0.2,str(self.pos+1)+'.')
		c.drawImage(self.img_path,l_w+ x_border,-last_shift/2+ name_obj.y-(d+self.image_H)*(self.pos+1), width=new_image_width, height=new_image_height)
	def calcWidth(self,h):
		self.image_H=h
		numb_size=self.image_H/1
		if self.pos==9:
			k1=stringWidth('1',self.fontName,numb_size)
		else:
			k1=0
		image_width, image_height = self.image.size
		k=h/image_height
		hh=k*image_width
		numb_size=self.image_H/1
		l_w=stringWidth(str(self.pos+1)+'.',self.fontName,numb_size)
		if hh>W-2*x_border-l_w*2-k1:
			print("MEASURED",self.pos+1)
			self.image_W=W-2*x_border-l_w*2-k1
		else:
			print("DEF WIDTH",self.pos+1)
			self.image_W=hh
		self.k=self.image_W/image_width
		self.orig_w=image_width
	def getWidth(self):
		pass
	def getHeight(self):
		pass

class Name:
	def __init__(self, s_name):
		self.s_name = s_name
		self.lines=split_string(s_name,0,user_path)
		if '' in self.lines:
			self.lines.remove('')
		self.fontName='brand_font'
		self.fontSize=20
		self.x=W/2
		self.y=H-y_border*1.5
		self.k=0.7
	def drawSelf(self,last_shift):
		#c.line(0,self.y,100,self.y)
		for i in range(len(self.lines)):
			c.setLineWidth(0.1)
			self.y=self.y-self.getHeight()*i-2*(i)
			c.setStrokeColorRGB(255,0,0)
			#c.rect(self.x-self.getWidth(self.lines[i])/2,self.y-self.getHeight()*i,self.getWidth(self.lines[i]),self.getHeight())
			textobject1 = c.beginText(self.x-self.getWidth(self.lines[i])/2,-last_shift/2.4 + self.y+2)
			textobject1.setCharSpace(0)
			textobject1.setFont(self.fontName, self.fontSize)
			textobject1.textLines(self.lines[i])
			c.drawText(textobject1)
			
			
	def getWidth(self,i):
		return stringWidth(i,self.fontName,self.fontSize)
	def getHeight(self):
		return self.fontSize*self.k
	def calcWidth(self):
		mx=0
		mx_buf=''
		for i in self.lines:
			if len(i)>mx:
				mx_buf=i
		while stringWidth(mx_buf,self.fontName,self.fontSize)>W-x_border*2:
			self.fontSize-=.1
		self.y=self.y-self.getHeight()
	def getY2(self):
		return W-y_border-self.getHeight()*2
	def getH(self):
		return self.getHeight()*len(self.lines)

	
def create_pdf(name, lines_list, filename):
	
	#c.rect(x_border,y_border,W-x_border*2,H-y_border*2)
	name_obj.calcWidth()
	
	p=0
	if n<8:
		p=1.5*cm
	name_obj.drawSelf(p)
	dH=name_obj.y-y_border-p
	#c.rect(0,y_border,W,dH)
	d=2
	h_per_name=dH/(n)-d
	if h_per_name>12:
		h_per_name=12
		d=dH/n-12
	print(h_per_name)
	mn=999
	for i in lines_obj:
		i.calcWidth(h_per_name)
		if i.k<mn:
			mn=i.k
	for i in lines_obj:
		i.k=mn
		i.drawSelf(d,p)
	

# Определяем путь к текущему файлу
current_directory = Path(__file__).resolve()

# Путь к файлу kek.ttf
#print(current_directory.parent / 'fonts' / 'kek.ttf')
pdfmetrics.registerFont(TTFont('brand_font', current_directory.parent/'fonts/'/'RainTungesten.ttf'))
pdfmetrics.registerFont(TTFont('list_font', current_directory.parent/'fonts/'/'testset.ttf'))
pdfmetrics.registerFont(TTFont('numb_font', current_directory.parent/'fonts/'/'Ultimate.ttf'))
n = 10
W=4.7*cm
H=4.5*cm
x_border=.15*cm
y_border=.1*cm
font_size = 300
font_path = "fonts/arnamu.ttf"
brandy=False

title_str=sys.argv[1]
print('title',title_str)
n=(len(sys.argv)-2)/3
j=sys.argv[2:]
buf=[]
lines_data=[]
for i in range(len(j)):
	if (i+1)%3==0:
		buf.append(j[i])
		lines_data.append(buf)
		print(buf)
		buf=[]
		
	else:
		buf.append(j[i])
print(n)
buf_check=lines_data[0][0]
for i in range(len(lines_data)):
	if buf_check == lines_data[i][0]:
		if i==len(lines_data)-1:
			brandy=True
	else:
		break
print(brandy)
lines_obj=[]
cache_folder='cache_folder/'
for i in rg(lines_data):
	lines_obj.append(_lines(i,lines_data[i][0],lines_data[i][1],lines_data[i][2]))
elements = title_str.split(',')
name_obj = Name(elements[0])

c = Canvas("ToPrint/set_label.pdf", pagesize=(W, H))

create_pdf(name_obj, lines_obj, "ToPrint/set_label.pdf")
c.save()
path_print="set_label.pdf"
subprocess.run(['ToPrint\\print_script_set.bat', path_print], shell=True)
#os.remove("ToPrint/set_label.pdf")
