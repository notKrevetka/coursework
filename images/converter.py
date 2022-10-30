from pdf2image import convert_from_path


images = convert_from_path('Raven.pdf')

for i in range(3, len(images)):
    letter = chr(65 + (i-3)//12)
    num = (i-3)%12 + 1 
    images[i].save("images\\"+ letter + str(num) +'.jpg', 'JPEG')

