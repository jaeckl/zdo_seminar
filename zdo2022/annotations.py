import cv2
import matplotlib.pyplot as plt
from skimage import transform
from . import processing
from . import io
class Builder:
    """ This class is used to build the annotation file. 
    It uses the data streaming pattern to create the file."""
    def __init__(self):
        self.file_name   = []
        self.frame_id    = []
        self.object_id   = []
        self.x_px        = []
        self.y_px        = []
        self.annot_timestamp = []
    def append(self,file_name,frame_id,object_id,x_px,y_px):
        """ Appends a new entry to the annotation file."""
        self.file_name.append(file_name)
        self.frame_id.append(frame_id)
        self.object_id.append(object_id)
        self.x_px.append(x_px)
        self.y_px.append(y_px)
        self.annot_timestamp.append(None)
    def build(self):
        """ Returns the whole annotation data as a dictionary."""
        return {
        "filename":self.file_name,
        "frame_id":self.frame_id,
        "object_id":self.object_id,
        "x_px":self.x_px,
        "y_px":self.y_px,
        "annotation_timestamp":self.annot_timestamp}


def annotate_video(video_filename, verbose=False, save_video=False):
    ano = Builder()
    cap = cv2.VideoCapture(video_filename)
    first_frame = True
    index = 0
    # Read until video is completed

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = transform.rescale(frame, 0.25, multichannel=True)

            # Display the resulting frame
            if first_frame:
                first_frame = False
                reference_frame = frame.copy()

            _, masked_frame = processing.extract_object(reference_frame, frame)
            y, x = processing.calculate_point(masked_frame)
            processing.create_patchedframe(verbose, save_video, index,
                                fig, ax, frame, y, x)
            ano.append(video_filename, index, 0, x/0.25, y/0.25)

        else:
            break
        index += 1
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    if save_video:
        io.render_videofile()
    return ano.build()
