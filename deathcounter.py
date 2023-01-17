import cv2
import pytesseract
import pyautogui
import numpy as np
import time
import tkinter as tk
pytesseract.pytesseract.tesseract_cmd = 'D:\\Tesseract\\tesseract.exe'


def update_counter():
    # take screenshot using pyautogui
    image = pyautogui.screenshot()
    # Turn image grayscale
    image = cv2.cvtColor(np.array(image),cv2.COLOR_BGR2GRAY)
     # Image crop coodinates
    x=754
    y=500
    width=412
    height=90
    # Crop the image
    image = image[y:y+height, x:x+width]
    # Black and White processing
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Apply dilation and erosion to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Read text from image
    imgtext = pytesseract.image_to_string(image, lang='eng', config='--psm 11')
    if imgtext=="" :
        print("No text found")
        label.config(text="No text found")
        label.update()
    else:    
        print(imgtext)
        label.config(text=imgtext)
        label.update()

    # writing it to the disk using opencv
    cv2.imwrite("image1.png", image)
    print("Reached")
    root.after(5000, update_counter)
    

root = tk.Tk()
root.geometry("300x300")
root.title("Deathcounter")

label = tk.Label(root)
label.config(text="Deaths: 0")
label.config(font=("Arial", 15))
label.pack()
label.place(relx=.5, rely=.5, anchor="center")

root.after(5000, update_counter)
root.mainloop()
