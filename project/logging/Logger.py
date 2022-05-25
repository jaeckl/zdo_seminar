import matplotlib.pyplot as plt
import skimage

def visual_log(frame, mask, masked_frame, y, x):
    """ Visualizes the result of the tracking using matplotlib. The plots present display the active frame, the masked frame,and the points of interest.
    Args:
        frame: The active frame.
        mask: The mask of the active frame.
        masked_frame: The masked frame.
        frame_rem: The frame with removed colors.
        y: The y coordinate of the point of interest.
        x: The x coordinate of the point of interest.
    """
    plt.subplot(2,2,1)
    plt.title("Actual Frame")
    plt.imshow(frame)
    plt.plot(x,y,"o",markersize=4,markerfacecolor="green")
    plt.subplot(2,2,2)
    plt.title("Motion Mask")
    plt.imshow(skimage.img_as_float(mask),cmap="gray")
    
    plt.subplot(2,2,3)
    plt.title("Removed Colors")
    plt.imshow(masked_frame,cmap="gray")
  
    plt.pause(.1)
    plt.draw()

def text_log(vid, i, y, x):
    """ Prints the results of the tracking to the console.
    Args:
        vid: The video.
        i: The frame number.
        y: The y coordinate of the point of interest.
        x: The x coordinate of the point of interest.
    """
    print("{} / {}: {},{}".format(i,len(vid),x,y))