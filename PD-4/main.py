import argparse
import cv2 as cv


def slice(video_path, duration=40, seconds=True, show=False):
    cap = cv.VideoCapture(video_path)
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
        return

    fps = cap.get(cv.CAP_PROP_FPS)
    width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    if seconds:
        frames = int(duration*fps)
    else:
        frames = duration
    part = None
    frame_n = -1
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            frame_n += 1
            if frame_n % frames == 0:
                part = cv.VideoWriter(f'{".".join(video_path.split(".")[:-1])}_part_{frame_n//frames+1}.avi', cv.VideoWriter_fourcc('M','J','P','G'), fps, (width, height))
            part.write(frame)
            
            if show:
                cv.imshow('Frame',frame)
                if cv.waitKey(int(1000/fps)) & 0xFF == ord('q'):
                    break
        else: 
            break

    cap.release()
    cv.destroyAllWindows()

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--frames', action=argparse.BooleanOptionalAction,
        help='If flag is selected then duration is in frames')
    parser.add_argument('video_path', nargs=1, help='Path to video')
    parser.add_argument('duration', nargs=1, type=int, help='Duration of segements in '
        'seconds. If -f flag is present then duration is in frames.')
    args = parser.parse_args()
    video_path = args.video_path[0]
    duration = args.duration[0]
    frames = args.frames
    print('Slicing...')
    slice(video_path, duration, not frames, True)
    print('Done!')
    
    
if __name__ == '__main__':
    run()