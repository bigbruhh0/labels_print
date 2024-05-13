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

_type=sys.argv[1]
def main(file_path,width,height):
	k=0
	f=file_path
	b_f=file_path	
	dy=0
	dx=0
	for i in range(5):
		if _type=='x':
			dx=-4+(i)*2
		else:
			dy=-4+(i)*2
		print(dx,dy)
		c = Canvas(f+'.pdf', pagesize=(_W,_H))
		#i.draw_rect_border(c)
		#c.rect(v_border,h_border,_W-v_border*2,_H-h_border*2)
		c.setStrokeColorRGB(0, 255, 0)
		c.drawString(_W/2-20,_H/2,'dx='+str(dx))
		c.drawString(_W/2-20,_H/2-10,'dy='+str(dy))
		c.rect(x_b+dx,y_b+dy,_W-x_b*2,_H-y_b*2)
		c.save()
		print("Направлено на печать:",f.replace(print_folder,'')+'.pdf')
		path_print="C:\\Users\\User\\Documents\\GitHub\\labels_print\\"+f+'.pdf'
		subprocess.run(['ToPrint\\print_script.bat', path_print], shell=True)
		os.remove(f+'.pdf')

_W=2.5*cm
_H=1.8*cm
x_b=.1*cm
y_b=.1*cm
print_folder='ToPrint/'
main(print_folder+'kekis_check.pdf',_W,_H)

