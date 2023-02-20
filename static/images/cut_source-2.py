import fitz
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path

doc = fitz.open('source-3.pdf')
page = doc[0]
pix = page.get_pixmap()
img = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
print(img)
plt.imshow(img, cmap='gray')

def save_array_as_image(file_path, arr, target_shape=None):
    Path(file_path).parents[0].mkdir(parents=True, exist_ok=True)
    img = Image.fromarray(arr.astype('uint8')).convert('L')
    img = (img>128)*255
    if target_shape is not None:
        img = img.resize(
            target_shape,
            resample=Image.Resampling.NEAREST
        )
    img.save(file_path)

save_array_as_image('picture.jpg', img)