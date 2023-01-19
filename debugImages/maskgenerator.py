import cv2
import numpy as np
import json
import sys
import os

# This script is based on this forum post: https://answers.opencv.org/question/134248/how-to-define-the-lower-and-upper-range-of-a-color/
image_hsv = None   # global ;(
pixel = (20,60,80) # some stupid default
data = {'lower': [-1,-1,-1], 'pixel': [-1,-1,-1], 'upper': [-1,-1,-1]}
## TODO: Refactor program so that it doesnt generate unneccessary .json files and just merges them instantly
def mergeJson():
    filenames = []
    for i in range(1,int(sys.argv[3])+1):
        filenames.append("generatedMasks\\"+ sys.argv[2] +"_"+ str(i) + ".json")
    
    print(filenames)
    
    json_files = []
    
    for filename in filenames:
        with open(filename) as json_file:
            data = json.load(json_file)
        json_files.append(data)
    
    with open("generatedMasks\\"+"merged_" + sys.argv[2] + ".json", "w") as f:
        f.write(json.dumps(json_files))
    
    for filename in filenames:
        os.remove(filename)
    
    exit()

def exportData():
    global data
    global numberOfMasks
    print("Exporting data ...")
    json_obj = json.dumps(data)
    if numberOfMasks != 0:
        with open("generatedMasks\\" + sys.argv[2] + "_"+ str(numberOfMasks) +".json", "w") as f:
            f.write(json_obj)
        cv2.destroyWindow("mask")
        numberOfMasks = numberOfMasks -1
        if numberOfMasks == 0:
            mergeJson()
        return
    else:       
        cv2.destroyAllWindows()

def closeMask(event, x,y, flags, param):
    if event== cv2.EVENT_RBUTTONDOWN:
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
    
    global image_hsv, pixel, numberOfMasks, merge_numberOfMasks  # so we can use it in mouse callback
    
    if len(sys.argv) < 4:
        print("Usage: python maskgenerator.py <input_file> <export_file> <number of exported masks>")
        print("export file without .json")
        exit(0)
        
    if int(sys.argv[3]) < 1:
          print("Usage: python maskgenerator.py <input_file> <export_file> <number of exported masks>")
          print("Plase enter a valid amount of masks")
          exit(0)
    
    image_src = cv2.imread(sys.argv[1])  # pick.py my.png
    if image_src is None:
        print ("the image read is None............")
        return

    numberOfMasks = int(sys.argv[3])

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