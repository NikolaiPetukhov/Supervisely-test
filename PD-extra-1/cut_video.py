import argparse
import random
import sys
import cv2 as cv


def cut(video_path, start, duration, save_path, in_frames=False):
    cap = cv.VideoCapture(video_path)
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
        return False
    width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv.CAP_PROP_FPS)
    frame_count = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    if start == 'random':
        if in_frames:
            start = random.randint(0, frame_count-int(duration))
        else:
            start = random.random()*(frame_count/fps)

    if in_frames:
        start_frame = int(start)
        duration_frames = int(duration)
    else:
        start_frame = int(float(start)*fps)
        duration_frames = int(duration*fps)

    out = cv.VideoWriter(save_path, cv.VideoWriter_fourcc('M','J','P','G'), fps, (width, height))
    for _ in range(start_frame):
        ret, _ = cap.read()
        if not ret == True:
            break
    for _ in range(duration_frames):
        ret, frame = cap.read()
        if not ret == True:
            break
        out.write(frame)
    cap.release()
    return True


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_path', nargs=1, help='Path to video')
    parser.add_argument('start', nargs=1, help='Point from where to start in frames or seconds. "random" for random')
    parser.add_argument('duration', nargs=1, type=float, help='Duration in frames or seconds')
    parser.add_argument('save_path', nargs=1, help='Path to save video')
    parser.add_argument('-f', '--frames', action=argparse.BooleanOptionalAction,
        help='If flag is selected then start and duration is in frames')
    args = parser.parse_args()
    video_path = args.video_path[0]
    start = args.start[0]
    duration = args.duration[0]
    save_path = args.save_path[0]
    in_frames = args.frames

    print('Cutting...')
    succes = cut(video_path, start, duration, save_path, in_frames)
    if succes:
        print('Done!')
        sys.exit(0)
    else:
        print('Error')
        sys.exit(1)


if __name__=='__main__':
    run()