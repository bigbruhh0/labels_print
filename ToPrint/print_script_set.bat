@echo off 
setlocal enabledelayedexpansion 
 
rem Set the argument passed from Python as arg1 
set arg1=%1 
echo "%arg1%"
 
rem Path to SumatraPDF.exe 
set "sumatra_path=%USERPROFILE%\Documents\GitHub\labels_print\ToPrint\SumatraPDF.exe" 
set "printer_name=TOSHIBA_SET"
rem Print the PDF file using SumatraPDF 
"%sumatra_path%" -print-to "%printer_name%" -print-settings "fit,landscape" "%USERPROFILE%\Documents\GitHub\labels_print\ToPrint\%arg1%"
