import cv2
import numpy as np

# THIS SCRIPT WAS NOT WRITTEN BY ME SOURCE: https://answers.opencv.org/question/134248/how-to-define-the-lower-and-upper-range-of-a-color/
image_hsv = None   # global ;(
pixel = (20,60,80) # some stupid default

def closeMask(event, x,y, flags, param):
    if event== cv2.EVENT_RBUTTONDOWN:
        cv2.destroyWindow("mask")

# mouse callback function
def pick_color(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y,x]

        #you might want to adjust the ranges(+-10, etc):
        upper =  np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
        lower =  np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
        print(pixel, lower, upper)

        image_mask = cv2.inRange(image_hsv,lower,upper)
        cv2.imshow("mask",image_mask)
        cv2.setMouseCallback("mask", closeMask )
    elif event == cv2.EVENT_RBUTTONDOWN and cv2.getWindowProperty("mask", cv2.WND_PROP_VISIBLE) != -1:
        cv2.destroyWindow("mask")

def main():
    import sys
    global image_hsv, pixel # so we can use it in mouse callback

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