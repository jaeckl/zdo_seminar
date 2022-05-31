class Builder:
    """ This class is used to build the annotation file. 
    It uses the data streaming pattern to create the file."""
    def __init__(self):
        self.file_name   = []
        self.frame_id    = []
        self.object_id   = []
        self.x_px        = []
        self.y_px        = []
    def append(self,file_name,frame_id,object_id,x_px,y_px):
        """ Appends a new entry to the annotation file."""
        self.file_name.append(file_name)
        self.frame_id.append(frame_id)
        self.object_id.append(object_id)
        self.x_px.append(x_px)
        self.y_px.append(y_px)
    def build(self):
        """ Returns the whole annotation data as a dictionary."""
        return {
        "file_name":self.file_name,
        "frame_id":self.frame_id,
        "object_id":self.object_id,
        "x_px":self.x_px,
        "y_px":self.y_px,
        "annotation_timestamp":[]}