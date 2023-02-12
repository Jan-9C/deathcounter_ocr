import cv2
import json
import sys



image_rgb = None   
crop = {'x': '754', 'y': '500', 'width': '412', 'height': '90'}
cropXend = 0
cropYend = 0

# mouse callback function
def pick_crop(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        crop['x'] = str(x)
        crop['y'] = str(y)
        print(f'Upper left corner: {x}, {y}')
        print("Waiting for right click on second corner ...")
    if event == cv2.EVENT_RBUTTONDOWN:
        print(f'Bottom right corner: {x}, {y}')
        cropXend = x
        cropYend = y
        crop['width'] = str(cropXend-int(crop['x']))
        crop['height'] = str(cropYend-int(crop['y']))

        print("Exporting JSON:")
        print(crop)
        with open('crops\\' + sys.argv[2] + ".json", 'w') as json_file:
            json_file.write(json.dumps(crop))
            exit(1)

def main():
    
    global image_rgb, crop # so we can use it in mouse callback

    if len(sys.argv) < 3:
        print("Missing parameter")
        print("Usage: python imageCrop.py <file> <filename>")
        exit(0) 

    image_src = cv2.imread(sys.argv[1])  # imageCrop.py my.png
    if image_src is None:
        print ("the image read is None............")
        exit(0)
    cv2.imshow("imageCrop",image_src)

    cv2.setMouseCallback('imageCrop', pick_crop)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__=='__main__':
    main()
