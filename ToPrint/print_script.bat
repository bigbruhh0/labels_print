@echo off 
setlocal enabledelayedexpansion 
 
rem Set the argument passed from Python as arg1 
set arg1=%1 
echo "%arg1%"
 
rem Path to SumatraPDF.exe 
set "sumatra_path=C:\Users\User\Documents\GitHub\labels_print\ToPrint\SumatraPDF.exe" 
 
rem Print the PDF file using SumatraPDF 
%sumatra_path% -print-to-default -print-settings "fit,landscape" "%arg1%"
