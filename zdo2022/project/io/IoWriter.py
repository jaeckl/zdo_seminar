import cv2
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json

def save_frame(dir,i,active_frame, y, x):
    """ Saves an image and draws a rectangle with the dimensions of 100x100 pixels around the point given by y and x. 
    
    Args:
        dir: The directory where the image is saved.
        i: The frame number.
        active_frame: The frame that is being annotated.
        y: The y-coordinate of the point.
        x: The x-coordinate of the point.
    """
    plt.figure()
    plt.imshow(active_frame)
    rect = patches.Rectangle((x-50, y-50), 100, 100, linewidth=2, edgecolor='r', facecolor='none')
    plt.gca().add_patch(rect)
    plt.savefig(os.path.join(dir,"frame_{}.png".format(str(i).rjust(6,'0'))))
    plt.close()

def save_video(dir,name):
    """ Creates a video from the images in the directory.
    Args:
        dir: The directory where the images are saved.
        name: The name of the video.
    """
    img_array = []
    for filename in glob.glob(os.path.join(dir,"frame_*.png")):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)


    out = cv2.VideoWriter(name,cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

def save_annotations(dictx):
    """ Saves the annotations to a json file.
    Args:
        dictx: The dictionary containing the annotations.
    """
    with open("annotations.json", "w") as outfile:
        json.dump(dictx,outfile,indent=4)