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
#brand_name,frag_name,conc,ml=['Dolce and Gabbana','LIGHT BLUE FOREVER POUR HOMME','edp','3']
brand_name=sys.argv[1]
frag_name=sys.argv[2]
conc=sys.argv[3]
ml=sys.argv[4]
class st:
	def __init__(self,_text,x,y,font,size,k,pos):
		self.text=_text
		self.x=x
		self.y=y
		self.fontName=font
		self.fontSize=50
		self.k=k
		self.pos=pos
		self.d=0
		self.size_d=0
		self.spacing=0
	def set_spacing(self):
		self.spacing=0
		if len(obj[3].max_line)>=10:
			w=self.getWidth()+self.spacing*(len(self.text)-1)
			while (w<_W-v_border*5):
				self.spacing+=.1
				w=self.getWidth()+self.spacing*(len(self.text)-1)
		if len(obj[3].max_line)<=10:
			self.spacing=self.spacing*.7
		
	def last_fix(self,d):
		H=d
		for i in obj[3].ln_text:
			H+=d+i.fontSize*i.k
		H=H+obj[1].y+obj[1].fontSize*obj[1].k
		return H
	def getWidth(self):
		self.width=stringWidth(self.text,self.fontName,self.fontSize)
		return self.width
	def getHeight(self):
		self.height=self.fontSize*self.k
		return self.height
	def draw_rect_border(self,c):
		c.setStrokeColorRGB(0,0,255)
		c.rect(self.x-self.getWidth()/2,self.d+obj[3].y+self.getHeight()*(self.pos)*(len(obj[3].ln_text)-1),self.getWidth(),self.getHeight())
	def draw_self(self, c, d,dd):
		H = self.last_fix(d)
		H = obj[0].y - H
		dh = H / 2
		global lazy_d
		lazy_d=dh
		#self.space=2
		if dev_draw:
			c.setLineWidth(0.2)
			c.line(0,self.get_pos(dh)[0],_W,self.get_pos(dh)[0])
			c.line(0,self.get_pos(dh)[1],_W,self.get_pos(dh)[1])
		self.fontSize = self.fontSize + self.size_d
		c.setFont(self.fontName, self.fontSize)
		textobject = c.beginText()
		textobject.setCharSpace(self.spacing)  # Установка межбуквенного интервала
		b=self.spacing*(len(self.text)-1)
		textobject.setFont(self.fontName, self.fontSize)
		textobject.setTextOrigin(self.x-(self.getWidth()+b)/2,dd+dh + self.d + obj[3].y + self.getHeight() * (self.pos) * (len(obj[3].ln_text) - 1))
		textobject.textLines(self.text)
		c.drawText(textobject)
	def get_pos(self,dh):
		return dh + self.d + obj[3].y + self.getHeight() * (self.pos) * (len(obj[3].ln_text) - 1),dh + self.d + obj[3].y + self.getHeight() * (self.pos) * (len(obj[3].ln_text) - 1)+self.getHeight()

		
class _Line:
	def __init__(self,_text, fontName, fontSize,_type):
		self.d=0
		self.text=_text
		self.fontName = fontName
		self.fontSize = fontSize
		self.x = _W/2
		self.y = _W/2
		self.k = .8
		self.len=len(self.text)
		self.type=_type
		self.width=200
		self.fontSize=30
		if self.type=="brand":
			self.fonts=['short_font','medium_font','medium_font']
			self.ks=[0.7,0.7,0.82]
			self.k=self.ks[0]
			self.fontName=self.fonts[0]
			#if self.len<=20:
			#	self.fontName='short_font'
			#	self.k=0.65
			#else:
			##	self.fontName='medium_font'
			#	self.k=0.65
		if self.type=="shop":
			self.fontName='info_font'
			self.k=.75
			self.fontSize=7.5
			self.y=h_border
		if self.type=="conc":
			self.fontName='info_font'
			self.k=.7
			self.fontSize=7.5
			self.y=h_border
		if self.type=="name":
			self.y=obj[1].y+obj[1].getH()
			self.lines=[]
			l=split_string(self.text)
			mx=0
			for i in l:
				if i!='':
					if len(i)>mx:
						mx=len(i)

					self.lines.append(i)
			self.lines=list(reversed(self.lines))
			self.ln_text=[]		
			if len(self.lines)>1:
				if mx>=10 and mx<=12:
					self.fontName='long_font'
					self.k=0.82
				elif mx>=12:
					self.fontName='long_font'
					self.k=0.82
				else:
					self.fontName='short_font'
					self.k=0.7
			else:
				if mx>6:
					self.fontName='long_font'
					self.k=0.82
				else:
					self.fontName='medium_font'
					self.k=0.7	
			l=[]
			
			for i in range(len(self.lines)):
				if self.lines[i]!='':
					self.ln_text.append(st(self.lines[i],self.x,self.y,self.fontName,self.fontSize,self.k,i))

				
	def getH(self):
		if self.type!='name':
			h=self.fontSize*self.k
		else:
			h=0
			for i in self.ln_text:
				
				h+=i.fontSize*i.k
		return h
	def draw_rect_border(self,c):
		if self.type!="name":
			c.setLineWidth(0.1)
			c.setStrokeColorRGB(255,0,0)
			#c.rect(self.x-self.getWidth()/2,self.y+self.d,self.getWidth(),self.getH())
		else:
			for i in self.ln_text:
				i.draw_rect_border(c)
	def get_pos(self):
		return self.y+self.d,self.y+self.getH()+self.d
	def getWidth(self,*li):
		if li:
			self.width=stringWidth(li[0],self.fontName,self.fontSize)
		else:
			self.width=stringWidth(self.text,self.fontName,self.fontSize)
		return self.width
	def calc_width(self,c):
		if self.type=="brand":
			if len(obj[3].ln_text)==1 and len(obj[3].ln_text[0].text)<11:
				self.fontSize=14
			else:
				self.fontSize=10
			MAX_H=self.fontSize*(self.k+.07)
			if stringWidth(self.text,self.fontName,self.fontSize)>_W:
				self.fontName=self.fonts[1]
				self.k=self.ks[1]
			if stringWidth(self.text,self.fontName,self.fontSize)>_W:
				self.fontName=self.fonts[2]
				self.k=self.ks[2]
			while self.getH()<MAX_H:
				self.fontSize+=.1
			while stringWidth(self.text,self.fontName,self.fontSize)>_W-v_border*2:
				self.fontSize-=.1
			self.y=_H-h_border-self.fontSize*self.k

		if self.type=="conc":
			self.y=obj[2].y+obj[2].getH()
		if self.type=="name":
			self.fontSize=50
			for i in self.ln_text:
				i.fontSize=50
			self.y=obj[1].y+obj[1].getH()
			
			mx=0
			mx_buf=''
			mn_buf=''
			if len(self.ln_text)>1:
				for i in range(len(self.ln_text)):
					if len(self.ln_text[i].text)>mx:
						mx=len(self.ln_text[i].text)
						if mx_buf=='':
							pass
						else:
							mn_buf=mx_buf
						mx_buf=self.ln_text[i].text
					else:
						mn_buf=self.ln_text[i].text
				self.max_line=mx_buf
				self.min_line=mn_buf
			else:
				self.max_line=self.ln_text[0].text
			while(self.getWidth(self.max_line)>_W-v_border*2):
				self.fontSize-=.1
				
				for i in self.ln_text:
					i.fontSize-=.1
			self.calc_height(c)
	def calc_height(self,c):
		if self.type=="name":
			self.dh=obj[0].y-obj[1].y-obj[1].getH()
			c.setStrokeColorRGB(255, 0, 0)
			#c.rect(0,obj[1].y+obj[1].getH(),_W,self.dh)
			
			for i in range(len(self.ln_text)):
				self.ln_text[i].y=self.y+self.fontSize*self.k-self.dh*(i)
			textH=0
			for i in self.ln_text:
				textH+=i.getHeight()
			
			while (textH>self.dh-free_h):
				for i in self.ln_text:
					i.fontSize-=.1
					
				textH=0
				for i in self.ln_text:
					textH+=i.getHeight()
			if len(self.ln_text)==1:
				for i in self.ln_text:
					if i.fontSize>24:
						i.fontSize=24
			#c.rect(v_border,1*(2+len(self.ln_text))+self.d+obj[1].y+obj[1].getH(),_W-2*v_border,self.dh-1*(2+len(self.ln_text))*2)
	def draw_self(self, c, d):
		dd=0
		if self.type!='brand' :
			for i in {'q','j','p','g'}:
				if i in self.text:
					dd=-1
		if self.type != 'name':
			
			c.setFont(self.fontName, self.fontSize)
			c.setFillColorRGB(0, 0, 0)
			#print(self.type,dd)
			textobject1 = c.beginText(self.x-self.getWidth()/2, self.y + self.d+dd)
			textobject1.setCharSpace(0)
			textobject1.setFont(self.fontName, self.fontSize)
			textobject1.textLines(self.text)
			c.drawText(textobject1)
			c.setLineWidth(0.2)
			if dev_draw:
				c.line(0,self.get_pos()[1],_W,self.get_pos()[1])
				c.line(0,self.get_pos()[0],_W,self.get_pos()[0])
		else:
			if len(self.ln_text)>1:
				for i in self.ln_text:
					i.set_spacing()
				mn=9999
				for i in self.ln_text:
					if i.spacing<mn:
						mn=i.spacing
			else:
				mn=0
			for i in self.ln_text:
				i.spacing=mn
				i.draw_self(c, d,dd)
	def shift(self,d,c):
		H=d
		for i in obj[3].ln_text:
			H+=d+i.fontSize*i.k
		H=H+obj[1].y+obj[1].fontSize*obj[1].k
		H = obj[0].y - H
		dh = H / 2
		if self.type=='conc':
			self.d=d+dh
		elif self.type=='shop':
			self.d=dh
		elif self.type=='name':
			for i in range(len(self.ln_text)):
				self.ln_text[i].d=d+d*(i+1)
		elif self.type=='brand':
			self.d=-d*0

def init_fonts():
	sh="Ornitons"
	sh_brand='VelaSansExtraBold'#GaretBook.ttf
	lg="steelfish"
	sh1="OrnitonsBold"
	sh2="Afrora"
	br_med="RainTungesten"
	conf="ConfigCondensedRegular"
	bold="ConfigCondenced"

	pdfmetrics.registerFont(TTFont('long_font', 'fonts/'+lg+'.ttf'))
	pdfmetrics.registerFont(TTFont('info_font', 'fonts/info_font.ttf'))
	pdfmetrics.registerFont(TTFont('bold_font', 'fonts/bold_font.ttf'))
	pdfmetrics.registerFont(TTFont('short_font', 'fonts/'+sh+'.ttf'))
	pdfmetrics.registerFont(TTFont('short1_font', 'fonts/'+sh1+'.ttf'))
	pdfmetrics.registerFont(TTFont('medium_font', 'fonts/'+br_med+'.ttf'))
	pdfmetrics.registerFont(TTFont('test_config', 'fonts/'+conf+'.ttf'))
	pdfmetrics.registerFont(TTFont('bold_font', 'fonts/'+bold+'.ttf'))
	pdfmetrics.registerFont(TTFont('sh_brand', 'fonts/'+sh_brand+'.ttf'))
	return 'long_font','info_font','bold_font','short_font','short1_font','medium_font'
def get_params():
	v_border=.1*cm
	h_border=.1*cm
	return v_border,h_border,2.5*cm,1.8*cm


def main(file_path,width,height):
	k=0
	f=file_path
	b_f=file_path
	if os.path.exists(f+'.pdfsdfsd'):
		pass
	else:
		
		c = Canvas(f+'.pdf', pagesize=(_W,_H))
		obj[0].calc_width(c)
		obj[1].calc_width(c)
		global free_h
		
		
		for i in obj:
			
			
			i.calc_width(c)
			i.calc_height(c)
		free_h=0
		for i in obj:
			free_h+=i.getH()
		free_h=_H-2*h_border-free_h
		d=free_h/(3+len(obj[3].ln_text))
		
		for i in obj:
			i.shift(d,c)
		
		obj[0].draw_self(c,d)
		obj[3].draw_self(c,d)
		dh=(obj[0].y-obj[3].ln_text[0].last_fix(d))/2
		obj[1].draw_self(c,d+lazy_d)
		obj[2].draw_self(c,d+lazy_d)
		#i.draw_rect_border(c)
		#c.rect(v_border,h_border,_W-v_border*2,_H-h_border*2)
		c.setStrokeColorRGB(0, 255, 0)

		conf = open(file_path+'.txt', "w")
		for i in obj:
			conf.write(str(i.type)+'/'+str(i.fontSize)+'/'+str(i.fontName)+'/'+str(i.k)+'/'+str(obj[3].ln_text[0].spacing)+'/'+'\n'+b_f)
		c.save()
		print("Направлено на печать:",f.replace(print_folder,'')+'.pdf')
		os.remove(f+'.pdf')
	#os.remove(str(b_f))

fonts=init_fonts()
obj=[]
lazy_d=0
dev_draw=False
v_border,h_border,_W,_H=get_params()
obj.append(_Line(brand_name,'Arial',9,'brand'))
obj.append(_Line(conc+" "+ml+" ml",'Arial',8,'conc'))
obj.append(_Line("АллюрПарфюм",'Arial',8,'shop'))
obj.append(_Line(frag_name,'Arial',10,'name'))
free_h=1.5*(2+len(obj[3].ln_text))
product_name=brand_name+frag_name
product_name=''.join(filter(str.isalnum, product_name))
#print(product_name)
print_folder='ToPrint/'
main(print_folder+product_name,_W,_H)

