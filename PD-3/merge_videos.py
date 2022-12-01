import os
import cv2 as cv
import numpy as np
from pathlib import Path


class Video:
    def __init__(self, cap, name):
        self.name = name
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

def _draw_text(img, text,
          pos=(0, 0),
          font=cv.FONT_HERSHEY_SIMPLEX,
          font_scale=1,
          text_color=(0, 255, 0),
          font_thickness=1,
          text_color_bg=(0, 0, 0)
          ):

    x, y = pos
    text_size, _ = cv.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv.rectangle(img, pos, (x + text_w, y + text_h + 1), text_color_bg, -1)
    cv.putText(img, text, (x, y + text_h - 1), font, font_scale, text_color, font_thickness)
    return img

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
            video = Video(cap, dir_entry.name)
            min_fps = min(min_fps, video.fps)
            min_duration = min(min_duration, video.duration)
            min_h = min(min_h, video.height)
            min_w = min(min_w, video.width)
            videos.append(video)
    
    ratio_w, ratio_h = tuple(int(x) for x in ratio.split(':'))
    x, y = _get_grid(len(videos), ratio_w, ratio_h, min_w, min_h)
    
    out = cv.VideoWriter(save_path, cv.VideoWriter_fourcc('M','J','P','G'), min_fps, (x*(min_w+4), y*(min_h+4)))
    
    for frame_n in range(int(min_duration*min_fps)):
        frame = np.zeros((y*(min_h+4), x*(min_w+4), 3), np.uint8)
        for i, video in enumerate(videos):
            pos = ((i//x)*(min_h+4), (i%x)*(min_w+4))
            
            ret, frame_part = video.cap.read()
            video.current_frame_n += 1
            while video.current_frame_n+1 < (video.fps / min_fps)*frame_n:
                ret, frame_part = video.cap.read()
                video.current_frame_n += 1
            
            if ret == True:
                # cut the frame in case it is bigger than expected
                frame_part = frame_part[0:min_h, 0:min_w]
                # add border
                t = np.zeros((min_h+4, min_w+4, 3), np.uint8)
                t[2:2+min_h,2:2+min_w] = frame_part
                frame_part = t
                # add video name 
                text_size, _ = cv.getTextSize(video.name, cv.FONT_HERSHEY_SIMPLEX, 1, 1)
                _draw_text(frame_part, video.name, (min_w-text_size[0]+1, min_h-text_size[1]))
                frame[pos[0]:pos[0]+min_h+4, pos[1]:pos[1]+min_w+4] = frame_part
            else:
                for v in videos:
                    v.cap.release()
                out.release()
                raise Exception("Cannot read next frame")

        out.write(frame)
        
    for v in videos:
        v.cap.release()
    out.release()