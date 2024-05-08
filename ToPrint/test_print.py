import win32print
import win32api
import os
import sys
from reportlab.lib.units import cm, inch
#print_pdf (входной pdf, режим печати, какой принтер)
#режим печати: 1 - односторонняя, 2 двойная по длинному краю, 3 - по короткому


def print_pdf(input_pdf, mode=2, printer=1):
	# тут мои принтеры, для своихузнаем имя дефолтного принтера через метод win32print.GetDefaultPrinter()
	name = "TOSHIBA_B-FV4_300dpi_copy4" #win32print.GetDefaultPrinter()
	try:
		# Устанавливаем дефолтный принтер
		win32print.SetDefaultPrinterW(name)
		win32print.SetDefaultPrinter(name)
	finally:
		# Если не получилось или получилось -&gt; устанавливаем этот принтер стандартом
		name = win32print.GetDefaultPrinter()

	# оставляем без изменений
	## тут нужные права на использование принтеров
	printdefaults = {"DesiredAccess": win32print.PRINTER_ALL_ACCESS}
	## начинаем работу с принтером ("открываем" его)
	handle = win32print.OpenPrinter(name, printdefaults)
	## Если изменить level на другое число, то не сработает
	level = 2
	## Получаем значения принтера
	attributes = win32print.GetPrinter(handle, level)
	## Настройка двухсторонней печати
	attributes['pDevMode'].Duplex = 1   #flip over  3 - это короткий 2 - это длинный край
	#attributes.Orientation = DMORIENT_PORTRAIT
	print(attributes['pDevMode'].PaperLength,attributes['pDevMode'].PaperWidth)
	attributes['pDevMode'].PaperLength = 160 # Variable
	attributes['pDevMode'].PaperWidth = 250 # Variable
	print(attributes['pDevMode'].PaperLength,attributes['pDevMode'].PaperWidth)

	## Передаем нужные значения в принтер
	win32print.SetPrinter(handle, level, attributes, 0)
	win32print.GetPrinter(handle, level)['pDevMode'].Duplex
	## Предупреждаем принтер о старте печати
	win32print.StartDocPrinter(handle, 1, [input_pdf, None, "raw"])
	## 2 в начале для открытия pdf и его сворачивания, для открытия без сворачивания поменяйте на 1
	win32api.ShellExecute(2,'print', input_pdf,'.','/manualstoprint',0)
	## "Закрываем" принтер
	win32print.ClosePrinter(handle)

	## Меняем стандартный принтер на часто используемый  
	win32print.SetDefaultPrinterW("TOSHIBA_B-FV4_300dpi_copy4")
	win32print.SetDefaultPrinter("TOSHIBA_B-FV4_300dpi_copy4")


# Печатаем документы

path_print = sys.argv[1]


print_pdf(path_print, 2, 0)
