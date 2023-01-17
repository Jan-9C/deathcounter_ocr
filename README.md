# deathcounter_ocr

A python script which detects death messages for games by using Optical Character Recognition.
<br /><br />

## Requirements:

## 1) Install Python 3

You can install the required version of python from the official [website](https://www.python.org/downloads/) or download it from the windows store.

## 2) Install Tesseract OCR

Install a version of Tesseract OCR [Download](https://github.com/UB-Mannheim/tesseract/wiki)

## 3) Install required pip libraries

```console
# pip install pytesseract
# pip install PyAutoGUI
# pip install opencv-python
# pip install numpy
```

# 4) Change set location of Tesseract OCR installation

In line 8 in deathcounter.py you have to change the path of tesseract.exe so that it matches the setup on your machine.

# Known Bugs

Dont Spam the Stop button this will lead to spamming the check function and therfore may increase your counter too much

Sometimes the detection goes wrong, for this reason you can change the counter by changing the content of the deaths.txt file or use the integrated button to manually change the value.
