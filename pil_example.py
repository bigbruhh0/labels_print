from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm

def text_to_image(text, font_size, width, height):
    # Создание изображения с белым фоном
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    
    # Загрузка шрифта
    font = ImageFont.truetype("arial.ttf", font_size)
    
    # Рисование текста на изображении
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    draw.text(((width - text_width) / 2, (height - text_height) / 2), text, font=font, fill="black")
    
    return image

def draw_stretched_text(pdf_file, width, height):
    c = canvas.Canvas(pdf_file, pagesize=(2.5*cm,1.8*cm))
    text = "Your text here"
    font_size = 12
    
    # Преобразование текста в изображение
    text_image = text_to_image(text, font_size, width, height)
    
    # Рисование изображения на канвасе
    c.drawImage(ImageReader(text_image), 0, 0)
    
    c.save()
w=int(2.5*cm)
h=int(1.8*cm)
draw_stretched_text("stretched_text_example.pdf", w, h)
