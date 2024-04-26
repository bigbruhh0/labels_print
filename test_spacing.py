
def add_image_to_pdf(image_path, pdf_path,y):
    # Открываем изображение с помощью Pillow
    image = Image.open(image_path)

    # Получаем ширину и высоту изображения
    image_width, image_height = image.size

    # Получаем ширину и высоту страницы PDF
    pdf_width, pdf_height = (4.5*cm,4.7*cm)

    # Вычисляем новую ширину изображения, чтобы подогнать его под ширину страницы PDF
    new_image_width = pdf_width

    # Вычисляем новую высоту изображения, сохраняя пропорции
    new_image_height = 10



    # Вставляем изображение на страницу PDF с подогнанными размерами
    c.drawImage(image_path, 0, y, width=new_image_width, height=new_image_height)





# Пример использования функции
# Пример использования функции

text = "Arboaoak kaksLSAKDФЫВJASHDKJASDЫВLASD"
image_path = "text_image.png"
font_size = 300
font_path = "fonts/testset.ttf"  # Путь к файлу шрифта, если необходимо использовать другой шрифт

create_text_image('1 Akro - Dark, edp', 'test1.png', font_size, font_path)
create_text_image("2 Jose Eisenberg - Ambre D'orient, edp", 'test2.png',font_size, font_path)
create_text_image("3 Christian Dior - Ambre Nuit, edp", 'test3.png',font_size, font_path)
image_path = "text_image.png"  # Путь к вашему изображению
pdf_path = "text_pdf.pdf"
# Создаем новый PDF-документ с форматом страницы letter
c = canvas.Canvas(pdf_path, pagesize=(4.5*cm,4.7*cm))
add_image_to_pdf('test1.png', pdf_path,0)
add_image_to_pdf('test2.png', pdf_path,50)
add_image_to_pdf('test3.png', pdf_path,100)
c.save()
#add_smooth_image_to_pdf(image_path, pdf_path)
