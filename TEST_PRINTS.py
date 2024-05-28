import subprocess
a="Maison de L'Asie" 
b="Les Nuits de Bali"
c='parf'
d='10'
b=b.upper()
subprocess.run(['python', 'PDF_LABEL.pyw', a, b, c, d,'1','-2','1.5'], check=True)
