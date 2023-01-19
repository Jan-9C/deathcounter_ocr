import cv2
import numpy as np
import json
import sys

# THIS SCRIPT WAS NOT WRITTEN BY ME SOURCE: https://answers.opencv.org/question/134248/how-to-define-the-lower-and-upper-range-of-a-color/
image_hsv = None   # global ;(
pixel = (20,60,80) # some stupid default
data = {'lower': [-1,-1,-1], 'pixel': [-1,-1,-1], 'upper': [-1,-1,-1]}

def exportData():
    global data
    print("Exporting data to gmask.json")
    json_obj = json.dumps(data)
    with open("generatedMasks\\" + sys.argv[2] + ".json", "w") as f:
        f.write(json_obj) 
    cv2.destroyAllWindows()

def closeMask(event, x,y, flags, param):
    if event== cv2.EVENT_RBUTTONDOWN:
        cv2.destroyWindow("mask")
        exportData()

# mouse callback function
def pick_color(event,x,y,flags,param):
    global data
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]

        #you might want to adjust the ranges(+-10, etc):
        upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        print(lower, pixel, upper)
         
        array1 = lower
        array2 = pixel
        array3 = upper
        
        data = {'lower': array1.tolist(), 'pixel': array2.tolist(), 'upper': array3.tolist()}
      
        image_mask = cv2.inRange(image_hsv,lower,upper)
        cv2.imshow("mask",image_mask)
        cv2.setMouseCallback("mask", closeMask )
    

def main():
    
    global image_hsv, pixel  # so we can use it in mouse callback
    
    if len(sys.argv) < 3:
        print("Usage: python colorpicker.py <input_file> <export_file>")
        print("export file without .json")
        exit(0)
    
    image_src = cv2.imread(sys.argv[1])  # pick.py my.png
    if image_src is None:
        print ("the image read is None............")
        return

    ## NEW ##
    cv2.namedWindow('hsv')
    cv2.setMouseCallback('hsv', pick_color)

    # now click into the hsv img , and look at values:
    image_hsv = cv2.cvtColor(image_src,cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv",image_hsv)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()