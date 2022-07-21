import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
drr_file = "../SiddonClassLib/src/build/drr.txt"
data = np.loadtxt(drr_file)
data=data[::-1, :]
data_min = np.min(data)
data_max = np.max(data)
data = (data-data_min)/(data_max-data_min)*255

image_out = Image.fromarray(data.astype('uint8'))
img_as_img = image_out.convert("RGB")
img_as_img.save("spine1.jpg")
ans = plt.imshow(data, cmap=plt.cm.gray)
plt.colorbar()
plt.show()
print("down")
