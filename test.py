from keras.models import load_model
import cv2
import numpy as np
from PIL import Image

labels = [str(i) for i in range(10)] + [chr(i) for i in range(ord('A'), ord('Z')+1)] + [chr(i) for i in range(ord('a'), ord('z')+1)]

test_image = './a5.png'
model = load_model('model.h5')

img = Image.open(test_image)
np_img = np.array(img)
img = cv2.resize(np_img, (128, 128))
np_img = np.array(img)

np_img = np.mean(np_img, axis=2) # convert to grayscale
img = np.reshape(np_img, (1, 128, 128, 1))

pred = model.predict(img)
pred = np.argmax(pred)
print(labels[pred])

