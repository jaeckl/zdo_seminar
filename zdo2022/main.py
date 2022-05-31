from project.datastructs import Video,AnnotationBuilder
from project.logging import Logger
from project.preprocessing import Processor
from project.io import IoWriter


from skimage import transform
import sys
import argparse

def annotate_video(vid,ano,output="images",verbose_lvl= 0,begin=0,end=None):
    scalefactor = 0.25
    if end is None:
        end = len(vid)
    for i in range(begin,end):
        data = vid.get_frame(i)
        active_frame,_ = data

        if end and i >= end:
            break
        if i < begin:
            continue
        if i == begin:
            reference_frame = active_frame
            reference_frame = transform.rescale(reference_frame,scalefactor,multichannel=True)
            continue
        y, x = __one_step_frame(vid, output, verbose_lvl, scalefactor, i, active_frame, reference_frame)
        ano.append(vid.name,i,0,x/scalefactor,y/scalefactor)
    IoWriter.save_video(output,"out.avi")
    IoWriter.save_annotations(ano.build())

def __one_step_frame(vid, output, verbose_lvl, scalefactor, i, active_frame, reference_frame):
    active_frame = transform.rescale(active_frame,scalefactor,multichannel=True)
    mask, masked_frame = Processor.extract_object(reference_frame, active_frame)
    y, x = Processor.calculate_point(masked_frame)
    IoWriter.save_frame(output, i, active_frame, y, x)
    
    if verbose_lvl == 2:
        Logger.visual_log(active_frame, mask, masked_frame, y, x)
    if verbose_lvl >= 1:
        Logger.text_log(vid, i, y/scalefactor, x/scalefactor)
    return y,x



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='track the tool')
    parser.add_argument('path', metavar='p', type=str,default=None,
        help='path to the directory containing annotations.xml and images directory')
    parser.add_argument('--verbose', '-v', type=int, default=0)
    parser.add_argument('--begin', '-b', type=int, default=0)
    parser.add_argument('--end', '-e', type=int, default=None)

    args = parser.parse_args()
    path = args.path
    verbose_lvl = args.verbose
    begin = args.begin
    end = args.end

    if path is None:
        print("No path given")
        sys.exit()

    vid = Video.VideoFile(sys.argv[1])
    ano = AnnotationBuilder.Builder()
    annotate_video(vid,ano,verbose_lvl=verbose_lvl,begin=begin,end=end)
