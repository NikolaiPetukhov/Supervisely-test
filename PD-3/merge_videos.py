import os
import cv2 as cv
import numpy as np
from pathlib import Path


class Video:
    def __init__(self, cap):
        self.cap = cap
        self.fps = cap.get(cv.CAP_PROP_FPS)
        self.width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_count/self.fps
        self.current_frame_n = 0


def _get_grid(n, ratio_w, ratio_h, w, h):
    for i in range(n):
        x = i+1
        y = (n+x-1)//x
        if x*w*ratio_h >= y*h*ratio_w:
            return x, y
    return n, 1

def merge(videos_path, save_path, ratio='16:9'):
    """
    """
    videos = []
    min_fps = 10000
    min_duration = 60*60*100
    min_h = 10000
    min_w = 10000
    for dir_entry in os.scandir(Path(videos_path)):
        if dir_entry.is_file():
            cap = cv.VideoCapture(dir_entry.path)
            if (cap.isOpened()== False): 
                print("Error opening video stream or file")
                continue
            video = Video(cap)
            min_fps = min(min_fps, video.fps)
            min_duration = min(min_duration, video.duration)
            min_h = min(min_h, video.height)
            min_w = min(min_w, video.width)
            videos.append(video)
    
    ratio_w, ratio_h = tuple(int(x) for x in ratio.split(':'))
    x, y = _get_grid(len(videos), ratio_w, ratio_h, min_w, min_h)
    
    out = cv.VideoWriter(save_path, cv.VideoWriter_fourcc('M','J','P','G'), min_fps, (x*min_w, y*min_h))
    
    for frame_n in range(int(min_duration*min_fps)):
        frame = np.zeros((y*min_h, x*min_w, 3), np.uint8)
        for i, video in enumerate(videos):
            pos = ((i//x)*min_h, (i%x)*min_w)
            
            ret, frame_part = video.cap.read()
            video.current_frame_n += 1
            while video.current_frame_n+1 < (video.fps / min_fps)*frame_n:
                ret, frame_part = video.cap.read()
                video.current_frame_n += 1
            
            if ret == True:
                frame[pos[0]:pos[0]+min_h, pos[1]:pos[1]+min_w] = frame_part
            else:
                for v in videos:
                    v.cap.release()
                out.release()
                raise Exception("Cannot read next frame")
        out.write(frame)
        
    for v in videos:
        v.cap.release()
    out.release()