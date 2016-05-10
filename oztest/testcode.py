import Image
import numpy as np

im = Image.open('test.png')
im = im.convert('RGB')

data = np.array(im)
red, green, blue = data.T
replacementArea = (red > 230) & (blue > 230) & (green > 230)
data[..., :-1][replacementArea.T] = (255, 255, 255)

im2 = Image.fromarray(data)
im2.show()
