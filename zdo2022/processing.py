from skimage import color
from skimage import morphology
import numpy as np
import matplotlib.pyplot as plt
def remove_unwanted_color(img):
    """ Removes the unwanted color from the image by converting it to hsv, 
    removing the hue which is not close to dark red, and after returning 
    it to rgb format removing the green and blue channels.
    Args:
        img: The image to be processed.
    Returns:
        The processed image.
    """
    img = color.rgb2hsv(img)
    img[img[:,:,0] < 0.9] = [0,0,0]
    img[img[:,:,1] < 0.5] = [0,0,0]
    img = color.hsv2rgb(img)
    img[:,:,1] = 0
    img[:,:,2] = 0
    return img

def subtract_frames(reference_frame, active_frame, threshold=1e-1):
    """ Doing a naive background subtraction.
    Args:
        reference_frame: The reference frame.
        active_frame: The active frame.
        threshold: The threshold for the difference between the frames.
    Returns:
        The mask of the active frame.
    """
    reference_frame = color.rgb2gray(reference_frame)
    active_frame = color.rgb2gray(active_frame)
    return np.abs(reference_frame - active_frame) > threshold

def apply_mask(frame, mask):
    """ Applies the mask to the frame.
    Args:
        frame: The frame to be processed.
        mask: The mask to be applied.
    Returns:
        The processed frame.
    """
    masked = frame.copy()
    masked[np.invert(mask)] = [0,0,0]
    return masked


def extract_object(reference_frame, active_frame):
    """ Applies all necessary operations to the active frame to extract only the needle holder's colors
    Args:
        reference_frame: The reference frame.
        active_frame: The active frame.
    Returns:
        The mask of the active frame
        The masked frame.
    """
    mask = subtract_frames(reference_frame, active_frame)
    mask = morphology.binary_erosion(mask, morphology.disk(2))
    mask = morphology.binary_dilation(mask, morphology.disk(10))
    masked_frame = apply_mask(active_frame, mask)
    masked_frame = remove_unwanted_color(masked_frame)
    return mask, masked_frame


def calculate_point(masked_frame):
    """ Calculates the point of interest in the masked frame.
    Args:
        masked_frame: The masked frame.
    Returns:
        The y coordinate of the point of interest.
        The x coordinate of the point of interest.
    """
    points = np.argwhere(masked_frame > 0)
    midpoint = np.median(points, axis=0)
    y, x = midpoint[0], midpoint[1]
    return y, x


def create_patchedframe(verbose, save_video, index, fig, ax, frame, y, x):
    ''' Creates an image with the needle holder's position marked.Updates the figure, if verbose is True.'''
    if verbose or save_video:
        ax.imshow(frame)
        ax.patches = []
        ax.add_patch(plt.Rectangle((x-25, y-25), 50, 50,
                                   fill=False, edgecolor='red', linewidth=1))
        if save_video:
            fig.savefig("frame{:04d}.png".format(index))
        plt.pause(.1)
        plt.draw()
