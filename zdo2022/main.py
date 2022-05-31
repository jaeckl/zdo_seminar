
# moduly v lokálním adresáři musí být v pythonu 3 importovány s tečkou
from . import podpurne_funkce
from . import annotations

class InstrumentTracker():
    def __init__(self):
        pass
    def predict(self, video_filename):
        """
        :param video_filename: name of the videofile
        :return: annnotations
        """
        return annotations.annotate_video(video_filename)
