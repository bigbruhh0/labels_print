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
		print(self.getHeight(),self.x,self.getWidth(),self.fontSize)
	def draw_self(self,c,d):
		H=self.last_fix(d)
		H=obj[0].y-H
		dh=H/2/2
		self.fontSize=self.fontSize+self.size_d
		c.setFont(self.fontName,self.fontSize)
		print(self.fontName,self.fontSize)
		print('draw',self.fontSize)
		c.drawCentredString(self.x,dh+self.d+obj[3].y+self.getHeight()*(self.pos)*(len(obj[3].ln_text)-1),self.text)
		print('testname',self.d)
		print(self.pos,self.getHeight())
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
		self.fontSize=12
		if self.type=="brand":
			if self.len<=15:
				self.fontName='short_font'
				self.k=0.65
			else:
				self.fontName='medium_font'
				self.k=0.65
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
			print(mx,'max')
			self.ln_text=[]		
			if len(self.lines)>1:
				if mx<=12:
					self.fontName='medium_font'
					self.k=0.7
				elif mx<12:
					self.fontName='medium_font'
					self.k=.7
				else:
					self.fontName='long_font'
					self.k=0.8
			else:
				if mx>6:
					self.fontName='long_font'
					self.k=0.8
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
				print(i.fontSize,h,i.fontSize*i.k)
		return h
	def draw_rect_border(self,c):
		if self.type!="name":
			c.setLineWidth(0.1)
			c.setStrokeColorRGB(255,0,0)
			#c.rect(self.x-self.getWidth()/2,self.y+self.d,self.getWidth(),self.getH())
		else:
			for i in self.ln_text:
				i.draw_rect_border(c)
	def getWidth(self,*li):
		if li:
			self.width=stringWidth(li[0],self.fontName,self.fontSize)
		else:
			self.width=stringWidth(self.text,self.fontName,self.fontSize)
		return self.width
	def calc_width(self,c):
		if self.type=="brand":
			self.fontSize=10
			while self.getWidth()>_W-v_border*2:
				self.fontSize-=.1
			self.y=_H-h_border-self.fontSize*self.k

		if self.type=="conc":
			self.y=obj[2].y+obj[2].getH()
		if self.type=="name":
			self.y=obj[1].y+obj[1].getH()
			self.fontSize=50
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
					print(i.fontSize)
				textH=0
				for i in self.ln_text:
					textH+=i.getHeight()
			self.fontSize=self.ln_text[0].fontSize
			#c.rect(v_border,1*(2+len(self.ln_text))+self.d+obj[1].y+obj[1].getH(),_W-2*v_border,self.dh-1*(2+len(self.ln_text))*2)
	def draw_self(self,c,d):
		print("HEAAIAIHGHT: ",self.getH())
		c.setFillColorRGB(0,0,0)
		if self.type!='name':
			c.setFont(self.fontName,self.fontSize)
			c.drawCentredString(self.x,self.y+self.d,self.text)
		else:
			for i in self.ln_text:
				i.draw_self(c,d)
	def shift(self,d,c):
		if self.type=='conc':
			self.d=d
		elif self.type=='name':
			for i in range(len(self.ln_text)):
				self.ln_text[i].d=d+d*(i+1)
				print(self.ln_text[i].d)
		elif self.type=='brand':
			self.d=-d*0

def init_fonts():
	sh="Ornitons"
	lg="steelfish"
	sh1="OrnitonsBold"
	sh2="Afrora"
	br_med="RainTungesten"
		

	pdfmetrics.registerFont(TTFont('long_font', 'fonts/'+lg+'.ttf'))
	pdfmetrics.registerFont(TTFont('info_font', 'fonts/info_font.ttf'))
	pdfmetrics.registerFont(TTFont('bold_font', 'fonts/bold_font.ttf'))
	pdfmetrics.registerFont(TTFont('short_font', 'fonts/'+sh+'.ttf'))
	pdfmetrics.registerFont(TTFont('short1_font', 'fonts/'+sh1+'.ttf'))
	pdfmetrics.registerFont(TTFont('medium_font', 'fonts/'+br_med+'.ttf'))
	return 'long_font','info_font','bold_font','short_font','short1_font','medium_font'
def get_params():
	v_border=.05*cm
	h_border=.15*cm
	return v_border,h_border,2.5*cm,1.8*cm


def main(file_path,width,height):
	k=0
	f=file_path
	while(os.path.exists(f)):
		k+=1
		f = file_path+'_'+str(k)+'.pdf'
	c = Canvas(f, pagesize=(_W,_H))
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
		i.draw_self(c,d)
		#i.draw_rect_border(c)
	#c.rect(v_border,h_border,_W-v_border*2,_H-h_border*2)
	c.setStrokeColorRGB(0, 255, 0)

	f = open('test_pdfs/test'+str(k)+'.txt', "w")
	for i in obj:
		f.write(str(i.type)+'/'+str(i.fontSize)+'/'+str(i.fontName)+'/'+str(i.k)+'/'+'\n')
	c.save()

fonts=init_fonts()
obj=[]
v_border,h_border,_W,_H=get_params()
obj.append(_Line(brand_name,'Arial',10,'brand'))
obj.append(_Line(conc+" "+ml+" ml",'Arial',8,'conc'))
obj.append(_Line("АллюрПарфюм",'Arial',8,'shop'))
obj.append(_Line(frag_name,'Arial',10,'name'))
free_h=1.5*(2+len(obj[3].ln_text))
main('test_pdfs/'+brand_name.replace(' ','_')+'___'+frag_name.replace(' ','_')+'.pdf',_W,_H)
