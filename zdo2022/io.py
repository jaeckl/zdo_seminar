import os 
import glob
import cv2

def render_videofile():
    img_array = []
    size = None
    for filename in glob.glob("frame*.png"):
        img = cv2.imread(filename)
        height, width, _ = img.shape
        size = (width, height)
        img_array.append(img)
    out = cv2.VideoWriter(
        'output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    for filename in glob.glob("frame*.png"):
        os.remove(filename)