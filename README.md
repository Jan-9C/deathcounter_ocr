# deathcounter_eldenring_ocr

A python script which detects death messages for Elden Ring by using **O**ptical **C**haracter **R**ecognition.
The number of deaths is then displayed in a graphical user interfaces. The number of deaths is saved between sessions. <br/>
The deathcounter doesn't interact with the game in any way and is therefore **compatible** with **online play**. <br/>
The deathcounter can be used for counting your deaths while livestreaming or just for yourself. <br/>
In my tests there was **no noticable performance impact**.

<br />

![Mask](./README_images/readmeMask.png)
![OCR ready](./README_images/readmeSuccessfull.png)

---

# How does it work?

Every 0.75 seconds the script takes a screenshot of your screen. The image gets cropped so that it only consists of the part of the screen where the death message appears. A mask corrosponding to the color of the death message gets generated. The mask is turned grayscale. After that the black and white values get filtered to be more readable for the OCR Algorithm. The processed image is then passed to the OCR algorithm and the result is passed to the counter.

# Requirements:

_The following installation guide is made with Windows in mind. If you use Linux I believe you will have no problem to get the script working even if the guide is made for windows._

## 1) Install Python 3 and PIP

As this is a python script you need a **working python installation** on your machine. <br/>
You can install the required version of python 3 from the [official website](https://www.python.org/downloads/) or download it from the microsoft store which is **easier** as it also installs **pip**. If you get python from the website you have to install pip seperately [(guide)](https://www.geeksforgeeks.org/how-to-install-pip-on-windows/).

## 2) Install Tesseract OCR

Install a version of **Tesseract OCR** [(Download)](https://github.com/UB-Mannheim/tesseract/wiki) <br/>
You only need to install the english language package, all of the other available things you can choose are not necessary

## 3) Install required pip libraries

```console
pip install pytesseract
```

```console
pip install PyAutoGUI
```

```console
pip install opencv-python
```

## 4) Change set location of Tesseract OCR installation

In **config.json** you have to change the path to tesseract.exe so that it matches the setup on your machine("tesseract_directory": "YOUR_PATH"). Remember to double every \

---

# Usage

Use the following command while having a Command Line Interface open in the directory the script is located:

```console
python deathcounter.py
```

or if you installed python from the official website:

```console
py deathcounter.py
```

If you want to show the counter while streaming you just have to add the window which displays the counter as a source in OBS.<br/>
If you want to reset the counter without spamming -1, you can just change the value of **deaths.txt**, which is located in the same directory as the script<br/>

---

# config.json

| Name                    | Value             | Usage                                                                                                                         |
| ----------------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| "tesseract_directory":  | directory path    | Use this to set the path to the directory your tesseract.exe is installed in                                                  |
| "refresh_time":         | time in ms        | Use this to configure the time the program waits between taking screenshots. Lower values lead could lead to better detection |
| "refresh_time_success": | time in ms        | Same as above but only gets used if a match is successfully detected                                                          |
| "debug_mode":           | enabled/disabled  | Will print debug messages to console and output images for debugging to debugImages\images if enabled                         |
| "compact_mode":         | enabled/disabled  | Will remove all elements of the counter except the number of deaths from the display window if enabled                        |
| "crop_file":            | name/path to file | Use to set the file which contains coodinates where image gets cropped (Standard: crop.json)                                  |

---

# Additional scripts

The debugImages folder contains two additional python scripts:<br/>

## cropimage.py

This script can be used to export the coordinates you want to crop from an image. You can change the config to match the exported file to change where the screenshot gets cropped. <br/>

Usage (without .json or directory):

```console
python cropimage.py <input file> <output file name>
```

1. **Left click** on the uppper left corner of the part you want to crop <br/>
2. **Right click** on the lower right corner of the part you want to crop <br/>
3. Crop coodinates get exported to debugImages/crops <br/>

## maskgenerator.py

⚠️ **This script is currently work in progress** ⚠️ <br/>

This script can be used to generate color masks which can be used in deathcounter.py to generate a complete mask which matches the death message. <br/>

Usage (without .json or directory):

```console
python maskgenerator.py <input file> <output file name> <number of exported masks>
```

1. **Left click** on the part of the image that you want to make a mask of
2. Inspect the opened windows which showcases what your mask would match
3. Either confirm the export by **rightclicking** the mask image or **close the window** and start at step one again
4. If you want to export a bigger number of masks repeat from step one

Currently the file only exports a single mask in a .json file. The implementation for importing them into deathcounter.py and the implementation for generating more masks at once is still work in progress.

---

# Known Issues

Sometimes the detection goes wrong, for this reason you can change the counter by changing the content of the deaths.txt file or use the integrated button to manually change the value. <br/>

The script only works if you use the resolution 1920x1080. If you use a different resolution you have to change the image crop coordinates, which can be configured by using the python script provided in debugImages\ and the config to crop out the correct part of the screen. <br/>

Currently only works with the english version of the game. <br/>
