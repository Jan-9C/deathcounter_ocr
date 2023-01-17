import cv2
import pytesseract
import pyautogui
import numpy as np
import tkinter as tk
import os
import time

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


running = True

# Function to generate levensthein distance between two Strings
# in other words it returns how much the strings differ
def levenshtein(s1, s2):
    m, n = len(s1), len(s2)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i
    for j in range(n + 1):
        d[0][j] = j
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
    return d[m][n]

    
def addDeath():
    current = 0
    with open(file_path,"r") as file:
        current = int(file.read())
    
    current = current + 1
    
    deathLabel.config(text=str(current))
    deathLabel.update()
    
    with open(file_path, "w") as file:
        file.write(str(current))

def subDeath():
    current = 0
    with open(file_path,"r") as file:
        current = int(file.read())
    
    current = current - 1
    
    deathLabel.config(text=str(current))
    deathLabel.update()
    
    with open(file_path, "w") as file:
        file.write(str(current))

def stop_scheduled_method():
    global running
    if running:
        running = False
        stopButton.config(text="Resume")
    else:
        running = True
        stopButton.config(text="Stop")
        update_counter()

def update_counter():
    detected = False
    # take screenshot using pyautogui
    image = pyautogui.screenshot()
    
    image = cv2.cvtColor(np.array(image),cv2.COLOR_BGR2HSV_FULL)
     # Image crop coodinates
    x=754
    y=500
    width=412
    height=90
    # Crop the image
    image = image[y:y+height, x:x+width]
   
    cv2.imwrite("cropped.png", image)
    
    # Lower Mask for testimage1 : 
    lower_red = np.array([176,183,102])
    upper_red = np.array([166,173,62])
    mask0 = cv2.inRange(image, lower_red, upper_red)
    
    # upper mask for testimage1:
    lower_red = np.array([166,173,62])
    upper_red = np.array([186,193,142])
    mask1 = cv2.inRange(image, lower_red, upper_red)
    
    # Lower Mask for testimage2: 
    lower_red = np.array([175,232,112])
    upper_red = np.array([165,222,72])
    mask2 = cv2.inRange(image, lower_red, upper_red)
    
    # upper Mask for testimage2 : 
    lower_red = np.array([165,222,72])
    upper_red = np.array([185,242,152])
    mask3 = cv2.inRange(image, lower_red, upper_red)
    
    
    
    
    
    mask = mask0+mask1+mask2+mask3
    
    output_img = image.copy()
    output_img[np.where(mask==0)] = 0
    
    image = output_img
    
    
    
    
    cv2.imwrite("mask.png", image)
    
    # Turn image grayscale
    image = cv2.cvtColor(np.array(image),cv2.COLOR_BGR2GRAY)
    cv2.imwrite("image_grayscale.png", image)
    
    # Black and White processing
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #Apply dilation and erosion to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Read text from image
    imgtext = pytesseract.image_to_string(image, lang='eng', config='--psm 11 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -c tessedit_pageseg_mode=1 -c tessedit_min_word_length=2')
    ldistance = levenshtein(imgtext,"YOUDIED")
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
        
        deathLabel.config(text=str(temp))
        deathLabel.update()
         # save image to disk
        cv2.imwrite("successfull.png", image)
        detected = True
        
    cv2.imwrite("unsuccessfull.png", image)

    if running & detected:
        root.after(10000, update_counter)
    elif running:
        root.after(1000, update_counter)
    

root = tk.Tk()
root.geometry("300x300")
root.config(bg="#1b1c1b")
root.title("Deathcounter")

titleLabel = tk.Label(root)
titleLabel.config(text="Deaths",font=("Times New Roman", 20), fg="#a01616", bg="#1b1c1b")
titleLabel.pack()
titleLabel.place(relx=.5, rely=.35, anchor="center")

deathLabel = tk.Label(root)
deathLabel.config(text=counter,font=("Times New Roman", 20), fg="#a01616", bg="#1b1c1b")
deathLabel.pack()
deathLabel.place(relx=.5, rely=.5, anchor="center")

stopButton = tk.Button(root)
stopButton.config(text="Stop", command=stop_scheduled_method, font=("Times New Roman", 10), fg="#a01616", bg="#1b1c1b")
stopButton.pack()
stopButton.place(relx=.5, rely=.7, anchor="center")

addButton = tk.Button(root)
addButton.config(text="+1", command=addDeath, font=("Times New Roman", 10), fg="#a01616", bg="#1b1c1b")
addButton.pack()
addButton.place(relx=.3, rely=.7, anchor="center")

subButton = tk.Button(root)
subButton.config(text="-1", command=subDeath, fg="#a01616", font=("Times New Roman", 10), bg="#1b1c1b")
subButton.pack()
subButton.place(relx=.7, rely=.7, anchor="center")

print("Updating starting...")
update_counter()
root.mainloop()