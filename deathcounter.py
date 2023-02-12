import cv2
import pytesseract
import pyautogui
import numpy as np
import tkinter as tk
import os
import json

#Fetch configs
with open('config.json', 'r') as f:
    config = json.load(f)

with open(config["crop_file"], 'r') as f:
    crop = json.load(f)

with open(config["mask_file"]) as f:
    mask_file = json.load(f)

tesseract_directory_path = config['tesseract_directory']
debug_mode = config['debug_mode']
compact_mode = config['compact_mode']
refresh_time = int(config['refresh_time'])
refresh_time_success = int(config['refresh_time_success'])
ocr_string = config["ocr_string"]
language = config["language"]
levenshtein_d = int(config["levensthein_d"])

counter = 0
running = False

# Set tesseract path to exe
pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_directory_path, "tesseract.exe")

# Initialize counter and deaths.txt
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "deaths.txt")

if not os.path.isfile("deaths.txt"):
    with open("deaths.txt", "w") as file:
        file.write("0")

with open(file_path,"r") as file:
    counter = file.read()

# Debug Info
if(debug_mode == "enabled"):
    print("Start Value of Counter: " + counter)

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

# increments the counter by 1 and saves the change to deaths.txt
def addDeath():
    current = 0
    with open(file_path,"r") as file:
        current = int(file.read())

    current = current + 1

    deathLabel.config(text=str(current))
    deathLabel.update()

    with open(file_path, "w") as file:
        file.write(str(current))

# decrements the counter by 1 and saves the change to deaths.txt
def subDeath():
    current = 0
    with open(file_path,"r") as file:
        current = int(file.read())

    current = current - 1

    if current >= 0:
        deathLabel.config(text=str(current))
        deathLabel.update()

        with open(file_path, "w") as file:
            file.write(str(current))

# Stop Button functionality
def stop_scheduled_method():
    global running
    if running:
        running = False
        stopButton.config(text="Start")
    else:
        running = True
        stopButton.config(text="Stop")
        update_counter()

# Looping method which checks for the death message and updates the counter accordingly
def update_counter():
    detected = False

    # take screenshot using pyautogui
    image = pyautogui.screenshot(region=(0, 0, 1920, 1080))
    image = cv2.cvtColor(np.array(image),cv2.COLOR_BGR2HSV_FULL)

    # Image crop coodinates
    x=int(crop["x"])
    y=int(crop["y"])
    width=int(crop["width"])
    height=int(crop["height"])

    # Crop the image
    image = image[y:y+height, x:x+width]

    # Debug Info
    if(debug_mode == "enabled"):
        cv2.imwrite("debugImages/images/cropped.png", image)

    firstMaskFetched = False;

    ## TODO: Optimize fetching of values so that it isnt executed everytime updateCounter() is called
    for element in mask_file:
        lower = np.array(element["lower"])
        pixelvalue = np.array(element["pixel"])
        upper = np.array(element["upper"])
        mask_lower = cv2.inRange(image, lower, pixelvalue)
        mask_upper = cv2.inRange(image, pixelvalue, upper)
        if firstMaskFetched:
            mask = mask + mask_lower + mask_upper
        else:
            mask = mask_lower + mask_upper
            firstMaskFetched = True;

    output_img = image.copy()
    output_img[np.where(mask==0)] = 0

    image = output_img

    # Debug Info
    if(debug_mode == "enabled"):
        cv2.imwrite("debugImages/images/mask.png", image)

    # Turn image grayscale
    image = cv2.cvtColor(np.array(image),cv2.COLOR_BGR2GRAY)

    # Debug Info
    if(debug_mode == "enabled"):
        cv2.imwrite("debugImages/images/image_grayscale.png", image)

    # TODO: Improve image processing? Probably not perfect?
    # Black and White processing
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    #Apply dilation and erosion to remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel, iterations=3)
    image = cv2.GaussianBlur(image, (5,5), 0)

    # Read text from image
    imgtext = pytesseract.image_to_string(image, lang=language, config='--psm 11 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -c tessedit_pageseg_mode=1 -c tessedit_min_word_length=2')

    # get levenshtein distance of complete cropped image
    ldistance = levenshtein(imgtext, ocr_string)

    # Get the shape of the image
    blackheight, blackwidth = np.shape(image)

    # Create a black image with the same shape as the input image
    black_image = np.zeros((blackheight, blackwidth, 3), dtype=np.uint8)
    black_image = cv2.cvtColor(np.array(black_image),cv2.COLOR_BGR2GRAY)

    # The following process generates 2 new images
    # One where the right halft is filled with black pixels and one where the left half is filled with black pixels
    # Overall this can help the OCR Algorithm as the simplifed images have less noise

    # Copy the image so that the right half can be filled with black pixels
    imageBlackR = image.copy()

    # Fill the left half of the image with black pixels
    imageBlackR[:, :width//2] = black_image[:, :width//2]

    # Debug Info
    if(debug_mode == "enabled"):
        cv2.imwrite("debugImages/images/imageBlackR.png", imageBlackR)

    # Copy the image so that the left half can be filled with black pixels
    imageBlackL = image.copy()

    # Fill the right half of the image with black pixels
    imageBlackL[:, width//2:] = black_image[:, width//2:]

    # Debug Info
    if(debug_mode == "enabled"):
        cv2.imwrite("debugImages/images/imageBlackL.png", imageBlackL)

    # Pass both processed simplified images to the OCR Algorithm
    righthalftext = pytesseract.image_to_string(imageBlackR, lang=language, config='--psm 11 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -c tessedit_pageseg_mode=1 -c tessedit_min_word_length=2')
    lefthalftext = pytesseract.image_to_string(imageBlackL, lang=language, config='--psm 11 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -c tessedit_pageseg_mode=1 -c tessedit_min_word_length=2')

    # Get the levensthein distance of the recognized text
    right_ldistance = levenshtein(righthalftext, ocr_string)
    left_ldistance = levenshtein(lefthalftext, ocr_string)

    # Choose the smallest levensthein distance as the true levenshtein distance / Choose the closest match
    ldistance = min(ldistance, right_ldistance, left_ldistance)

    # Debug Info
    if(debug_mode == "enabled"):
        print("Detected: " + lefthalftext + "|" + imgtext + "|" + righthalftext)
        print("ldistance: " + str(ldistance))

    # Check for acceptable levenshtein distance
    if ldistance >= levenshtein_d:
        # Debug Info
        if(debug_mode == "enabled"):
            print("No valid text found")
            cv2.imwrite("debugImages/images/unsuccessfull.png", image)

    elif ldistance < levenshtein_d:
        # Debug Info
        if(debug_mode == "enabled"):
            print("Valid Text found: " + lefthalftext + "|" + imgtext + "|" + righthalftext)

        detected = True
        addDeath()

        # Debug Info
        if(debug_mode == "enabled"):
             cv2.imwrite("debugImages/images/successfull.png", image)


    # If program is set to run by the button a match gets detected the program waits longer to schedule the match process again
    if running and detected:
        root.after(refresh_time_success, update_counter)
    elif running:
        root.after(refresh_time, update_counter)

# UI functionality
root = tk.Tk()
root.config(bg="#1b1c1b")
root.title("Deathcounter")

if compact_mode!="enabled":
    root.geometry("300x300")
else:
    root.geometry("250x50")

if compact_mode!="enabled":
    titleLabel = tk.Label(root)
    titleLabel.config(text="Deaths",font=("Times New Roman", 20), fg="#a01616", bg="#1b1c1b")
    titleLabel.pack()
    titleLabel.place(relx=.5, rely=.35, anchor="center")

    stopButton = tk.Button(root)
    stopButton.config(text="Start", command=stop_scheduled_method, font=("Times New Roman", 10), fg="#a01616", bg="#1b1c1b")
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

deathLabel = tk.Label(root)
deathLabel.config(text=counter,font=("Times New Roman", 20), fg="#a01616", bg="#1b1c1b")
deathLabel.pack()
deathLabel.place(relx=.5, rely=.5, anchor="center")
# Copyright Notice
print("")
print("deathcounter.py  Copyright (C) 2023  Jan 9-C \n\nThis program comes with ABSOLUTELY NO WARRANTY; \nThis is free software, and you are welcome to redistribute it \nunder certain conditions;\n\nSee the GNU General Public License for more details.")
print("")

print("Starting Counter ...")
update_counter()
root.mainloop()
