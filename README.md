# deathcounter>_eldenring_ocr

A python script which detects death messages for Elden Ring by using Optical Character Recognition.
The number of deaths is then displayed in a graphical user interfaces. The number of deaths is saved between sessions. <br/>
The deathcounter doesn't interact with the game in any way and is therefore compatible with online play. <br/>
The deathcounter can be used for counting your deaths while livestreaming or just for yourself. <br/>
In my tests there was no noticable performance impact.

<br /><br />

# How does it work?

Every 0.75 seconds the script takes a screenshot of your screen. The image gets cropped so that it only consists of the part of the screen where the death message appears. A mask corrosponding to the color of the death message gets generated. The mask is turned grayscale. After that the black and white values get filtered to be more readable for the OCR Algorithm. The processed image is then passed to the OCR algorithm and the result is passed to the counter.

# Requirements:

## 1) Install Python 3

You can install the required version of python 3 from the [official website](https://www.python.org/downloads/) or download it from the windows store.

## 2) Install Tesseract OCR

Install a version of Tesseract OCR [(Download)](https://github.com/UB-Mannheim/tesseract/wiki)

## 3) Install required pip libraries

```console
pip install pytesseract
pip install PyAutoGUI
pip install opencv-python
pip install numpy
```

## 4) Change set location of Tesseract OCR installation

In config.json you have to change the path to tesseract.exe so that it matches the setup on your machine("tesseract_directory": "YOUR_PATH"). Remember to double every \

# Usage

Use the following command while having a Command Line Interface open in the directory the script is located:

```console
python deathcounter.py
```

If you want to show the counter while streaming you just have to add the window which displays the counter as a source in OBS.

# Known Bugs

Spamming the stop button can lead to unintended changes in value

Sometimes the detection goes wrong, for this reason you can change the counter by changing the content of the deaths.txt file or use the integrated button to manually change the value.

The script only works if you use the resolution 1920x1080. If you use a diffrent resolution you have to change the image crop coordinates which start in line 87 to crop out the correct part of the screen.
