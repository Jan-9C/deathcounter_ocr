import cv2
import pytesseract
import pyautogui
import numpy as np
import time


pytesseract.pytesseract.tesseract_cmd = 'D:\\Tesseract\\tesseract.exe'

time.sleep(5)

# take screenshot using pyautogui
image = pyautogui.screenshot()

image = cv2.cvtColor(np.array(image),cv2.COLOR_BGR2GRAY)

# Image crop coodinates
x=754
y=500
width=412
height=90

image = image[y:y+height, x:x+width]

# Black and White processing
image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Apply dilation and erosion to remove noise
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)

text = pytesseract.image_to_string(image, lang='eng', config='--psm 11')
if text=="" :
    print("No text found")
else:    
    print(text)

# writing it to the disk using opencv
cv2.imwrite("image1.png", image)

