import os
from skimage import io
from lxml import etree
import pandas as pd


class VideoFile:
    """ This class is used as a container for video data. It stores the frames and annotation data
    """
    def __init__(self,filepath):
        """ Create a new VideoFile object from a directory containing images and annotations.
        """
        self.__load_annotations(os.path.join(filepath,"annotations.xml"))
        self.__load_frames(os.path.join(filepath,"images"))
        print(self.annotations["filename"].unique())
    
    def __len__(self):
        """ Returns the number of frames in the video."""
        return len(self.frames)
    
    def __getitem__(self, idx):
        """ Implementation of the enumerate function interface for the VideoFile class."""
        return self.get_frame(idx)

    
    def get_frame(self,frame_no):
        """ Retursn the frame given by the index."""
        delta_frame_id = str(frame_no + int(self.annotations.frame_id.iloc[0]))
        return self.frames[frame_no], self.annotations[
            self.annotations.frame_id == delta_frame_id
            ]
    
    def __load_annotations(self,path):
        """Internal method for loading the annotation data from the .xml file."""
        annotation={
            "filename": [], # pth.parts[-1]
            "frame_id": [],
            "object_id": [],
            "label": [],
            "x_px": [], # x pozice obarvených hrotů v pixelech
            "y_px": [],   # y pozice obarvených hrotů v pixelech
            "annotation_timestamp": [],
        }

        tree = etree.parse(path)
        self.name = tree.xpath("//name")[0].text
        updated = tree.xpath("//updated")[0].text # date of last change in CVAT

        for track in tree.xpath('track'):
            for point in track.xpath("points"):
                pts = point.get("points").split(",")
                x, y = pts
                annotation["filename"].append(path)
                annotation["object_id"].append(track.get("id"))
                annotation["x_px"].append(x)
                annotation["y_px"].append(y)
                annotation["label"].append(track.get("label"))
                annotation["frame_id"].append(point.get("frame"))
                annotation["annotation_timestamp"].append(updated)

        self.annotations = pd.DataFrame(annotation)
    
    def __load_frames(self,path):
        """ Internal method for loading the frames from the .png files."""
        self.frames = io.imread_collection(os.path.join(path,"frame_*.png"))
