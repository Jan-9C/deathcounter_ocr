import cv2
import numpy as np
import json

# THIS SCRIPT WAS NOT WRITTEN BY ME SOURCE: https://answers.opencv.org/question/134248/how-to-define-the-lower-and-upper-range-of-a-color/
image_hsv = None   # global ;(
pixel = (20,60,80) # some stupid default
maskOpened = False
data = {'lower': [-1,-1,-1], 'pixel': [-1,-1,-1], 'upper': [-1,-1,-1]}

def exportData():
    global data
    print("Exporting data to gmask.json")
    json_obj = json.dumps(data)
    with open("generatedMasks\gmask.json", "w") as f:
        f.write(json_obj) 

def closeMask(event, x,y, flags, param):
    global maskOpened
    if event== cv2.EVENT_RBUTTONDOWN:
        cv2.destroyWindow("mask")
        exportData()
        maskOpened = False

# mouse callback function
def pick_color(event,x,y,flags,param):
    global maskOpened
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
        maskOpened = True
        cv2.setMouseCallback("mask", closeMask )
    elif event == cv2.EVENT_RBUTTONDOWN and maskOpened:
        cv2.destroyWindow("mask")
        maskOpened = False
        exportData()

def main():
    import sys
    global image_hsv, pixel, maskOpened # so we can use it in mouse callback

    maskOpened = False
    
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