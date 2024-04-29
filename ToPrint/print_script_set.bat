@echo off 
setlocal enabledelayedexpansion 
rem Установка аргумента, переданного из Python, как arg1 
set arg1=%1 
rem Путь к SumatraPDF.exe 
set "sumatra_path=C:\Users\User\Documents\GitHub\labels_print\ToPrint\SumatraPDF.exe" 
rem Имя принтера 
set "printer_name=TOSHIBA_SET"
rem Печать PDF-файла с использованием SumatraPDF 
%sumatra_path% -print-to "%printer_name%" -print-settings "fit,landscape" "%arg1%"
