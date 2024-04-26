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
from functions import do_split, split_line, get_info, split_string,add_image_to_pdf,create_text_image
from pathlib import Path
from reportlab.pdfbase.pdfmetrics import stringWidth
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess
import sys
import os

def rg(spis):
	return range(len(spis))
def getHto(pos):
	h=0
	print('POS',pos)
	for i in range(pos+1):
		h+=lines_obj[i].getHeight()
		print(i,h)
	return h
class _lines:
	def __init__(self,pos, brand_name, frag_name, conc):
		self.pos=pos
		self.brand_name = brand_name
		self.frag_name = frag_name
		self.conc = conc
		print(self.brand_name,self.frag_name,self.conc)
		self.fontName=fonts[7-self.pos]
		print(self.fontName)
		self.text=str(pos+1)+'. '+self.brand_name+' - '+self.frag_name+', '+self.conc
		self.fontSize=12
		self.k=0.7
		self.x=x_border
		self.y=H
	def drawSelf(self,c):
		textobject = c.beginText()
		textobject.setCharSpace(0)  # Установка межбуквенного интервала
		textobject.setFont(self.fontName, self.fontSize)
		textobject.setTextOrigin(self.x,name_obj.y-getHto(self.pos))
		textobject.textLines(self.text)
		c.drawText(textobject)
	def calcWidth(self):
		while self.getWidth()>W-x_border*2:
			self.fontSize-=.1
	def getWidth(self):
		return stringWidth(self.text,self.fontName,self.fontSize)
	def getHeight(self):
		return self.fontSize*self.k

class Name:
	def __init__(self, s_name):
		self.s_name = s_name
		self.lines=split_string(s_name)
		if '' in self.lines:
			self.lines.remove('')
		self.fontName='brand_font'
		self.fontSize=24
		self.x=W/2
		self.y=H-y_border
		self.k=0.7
	def drawSelf(self,c):
		for i in range(len(self.lines)):
			c.setLineWidth(0.1)
			self.y=self.y-self.getHeight()*i
			c.setStrokeColorRGB(255,0,0)
			c.rect(self.x-self.getWidth(self.lines[i])/2,self.y-self.getHeight()*i,self.getWidth(self.lines[i]),self.getHeight())
			textobject1 = c.beginText(self.x-self.getWidth(self.lines[i])/2, self.y)
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
	c = Canvas(filename, pagesize=(W, H))
	c.rect(x_border,y_border,W-x_border*2,H-y_border*2)
	name_obj.calcWidth()
	name_obj.drawSelf(c)
	c.line(0,name_obj.getY2(),W,H-y_border-name_obj.getH()*len(name_obj.lines))
	mn=999
	for i in lines_obj:
		i.calcWidth()
		if i.fontSize<mn:
			mn=i.fontSize
	for i in lines_obj:
		i.fontSize=mn
		i.drawSelf(c)
	c.save()
# Определяем путь к текущему файлу
current_directory = Path(__file__).resolve()

# Путь к файлу kek.ttf
#print(current_directory.parent / 'fonts' / 'kek.ttf')
pdfmetrics.registerFont(TTFont('brand_font', current_directory.parent/'fonts/'/'RainTungesten.ttf'))
pdfmetrics.registerFont(TTFont('list_font', current_directory.parent/'fonts/'/'Ornitons.ttf'))
fonts=[]
for i in range(0,8):
	n=((i+1)*2)
	fonts.append('Roboto-Medium'+str(i)+'.ttf')
	bg='Roboto-Medium'+str((i+1)*2)+'.ttf'
	print(bg)
	pdfmetrics.registerFont(TTFont('Roboto-Medium'+str(i)+'.ttf', current_directory.parent/'fonts/'/'sets/'/bg))
n = 5
W=4.7*cm
H=4.5*cm
x_border=.2*cm
y_border=.2*cm
lines_data = [
    ["B1", "Fe3", "Co3"],
    ["Br2", "Fragnce3", "Conceion3"],
    ["Acqua di parma", "ACQUA NOBILE GELSOMINO", "edp"],
    ["Brand4", "Fragrance4", "Concentration4"],
    ["Brand5", "Fragrance5", "Concentration5"]
]
lines_obj=[]
for i in rg(lines_data):
	lines_obj.append(_lines(i,lines_data[i][0],lines_data[i][1],lines_data[i][2]))
	
name_obj = Name("LACOSTE L.12.12 WOMAN")

create_pdf(name_obj, lines_obj, "odutput.pdf")

