from pathlib import Path
import random
import cv2 as cv
import numpy as np
from matplotlib import colors


FOLDER = 'video_samples'
QUANTITY = 5
WIDTH = 320
HEIGHT = 180
DURATION = 10
FPS = 30
COLORS = ['blue', 'purple', 'red', 'green', 'orange', 'salmon', 'pink', 'gold',
            'orchid', 'slateblue', 'limegreen', 'seagreen', 'darkgreen', 'olive',
            'teal', 'aquamarine', 'steelblue', 'powderblue', 'dodgerblue', 'navy',
            'magenta', 'sienna', 'maroon']


def run(folder = FOLDER, q=QUANTITY, width=WIDTH, height=HEIGHT, duration=DURATION, fps=FPS):
    for i in range(q):
        video_color = tuple(int(c*255) for c in colors.to_rgb(random.choice(COLORS)))
        video_color = (video_color[2], video_color[1], video_color[0])
        
        if not Path(folder).exists():
            Path(folder).mkdir()

        out = cv.VideoWriter(f'{folder}/sample_{i+1}.avi', cv.VideoWriter_fourcc('M','J','P','G'), fps, (width, height))
        for frame_n in range(duration*fps):
            frame = np.zeros((height, width, 3), np.uint8)
            frame[0:height, 0:width] = video_color
            text = f'Video #{i+1}'
            cv.putText(frame, text, (0, 23), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0), 1)
            text = f'Frame: {frame_n}'
            cv.putText(frame, text, (0, 60), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,0), 1)
            out.write(frame)
        out.release()

if __name__ == '__main__':
    run()