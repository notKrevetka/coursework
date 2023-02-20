from pdf2image import convert_from_path


images = convert_from_path('source-3.pdf')

for i in range(0, len(images)):
    letter = chr(65 + (i)//12)
    num = (i)%12 + 1 
    images[i].save("images_source-3//"+ str('source-3__') + letter + str(num) +'.jpg', 'JPEG')

