from cv2 import threshold
import pytesseract
from PIL import Image

image = Image.open('code.jpg')
result = pytesseract.image_to_string(image)
image=image.convert('L')

threshold=170
table=[]
for i in range(256):
    if i<threshold:
        table.append(0)
    else :
        table.append(1)
image=image.point(table,'1')
image.show()
print(result)