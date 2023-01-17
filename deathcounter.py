import cv2
import pytesseract
import pyautogui
import numpy as np
import time
import tkinter as tk
import os

pytesseract.pytesseract.tesseract_cmd = 'D:\\Tesseract\\tesseract.exe'
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "deaths.txt")

if not os.path.isfile("deaths.txt"):
    with open("deaths.txt", "w") as file:
        file.write("0")

counter = 0

with open(file_path,"r") as file:
    counter = file.read()
    
print("Current Counter: " + counter)

# Function to generate levensthein distance between two Strings
# in other words it returns how much the strings differ
def levenshtein(s1, s2):
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    if s1[-1] == s2[-1]:
        cost = 0
    else:
        cost = 1
    return min(levenshtein(s1[:-1], s2) + 1,
               levenshtein(s1, s2[:-1]) + 1,
               levenshtein(s1[:-1], s2[:-1]) + cost)


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
    ldistance = levenshtein(imgtext,"YOU DIED")
    print("Detected: " + imgtext)
    print("ldistance: " + str(ldistance))
    
    # Check for acceptable levenshtein distance
    if ldistance > 6:
        print("No valid text found")
    elif ldistance < 6:    
        print("Valid Text found: " + imgtext)
        
        temp = 0
        
        with open(file_path,"r") as file:
            counter = file.read()
            temp = int(counter)
            
        temp = temp+1
        
        with open(file_path,"w") as file:
            file.write(str(temp))
        
        label.config(text=str(temp))
        label.update()

    # save image to disk
    cv2.imwrite("image1.png", image)
    root.after(5000, update_counter)
    

root = tk.Tk()
root.geometry("300x300")
root.title("Deathcounter")

titlelabel = tk.Label(root)
titlelabel.config(text="Deaths")
titlelabel.config(font=("Arial", 15))
titlelabel.pack()
titlelabel.place(relx=.5, rely=.3, anchor="center")

label = tk.Label(root)
label.config(text=counter)
label.config(font=("Arial", 15))
label.pack()
label.place(relx=.5, rely=.5, anchor="center")

root.after(5000, update_counter)
root.mainloop()
