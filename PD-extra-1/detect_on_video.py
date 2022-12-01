import argparse
import sys
from transformers import DetrFeatureExtractor, DetrForObjectDetection
import torch
from PIL import Image
import cv2 as cv
import random
from matplotlib import colors


COLORS = ['blue', 'purple', 'red', 'green', 'orange', 'salmon', 'pink', 'gold',
            'orchid', 'slateblue', 'limegreen', 'seagreen', 'darkgreen', 'olive',
            'teal', 'aquamarine', 'steelblue', 'powderblue', 'dodgerblue', 'navy',
            'magenta', 'sienna', 'maroon']


def draw_text(img, text,
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
    return text_size


def draw_bbox(img, bbox, text, color=(255,255,255), font=cv.FONT_HERSHEY_SIMPLEX, font_scale=1):
    cv.rectangle(img, bbox[:2], bbox[2:4], color, 2)
    text_coordinates = (bbox[0]+1, bbox[1]+1)
    draw_text(img, text, text_coordinates, font, font_scale, color, 1, (0,0,0))


def analyze_image(img, feature_extractor, model):

    inputs = feature_extractor(images=img, return_tensors="pt")
    outputs = model(**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    target_sizes = torch.tensor([img.size[::-1]])
    results = feature_extractor.post_process(outputs, target_sizes=target_sizes)[0]

    detections = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        detections.append((score, model.config.id2label[label.item()], tuple(round(i, 2) for i in box.tolist())))
    
    return detections


def detect_on_video(video_path, save_path, score=0.9):
    feature_extractor = DetrFeatureExtractor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    
    cap = cv.VideoCapture(video_path)
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")
        return False
    width  = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))    
    fps = cap.get(cv.CAP_PROP_FPS)

    out = cv.VideoWriter(save_path, cv.VideoWriter_fourcc('M','J','P','G'), fps, (width, height))

    colors_map = {}
    while True:
        ret, frame = cap.read()
        if ret == True:
            PIL_image = Image.fromarray(frame)
            detections = analyze_image(PIL_image, feature_extractor, model)
            for score, label, box in detections:
                if score > score:
                    if not label in colors_map.keys():
                        color = tuple(int(c*255) for c in colors.to_rgb(random.choice(COLORS)))
                        color = (color[2], color[1], color[0])
                        colors_map[label] = color
                    bbox = [int(i) for i in box]
                    draw_bbox(frame, bbox, label, colors_map[label])
            out.write(frame)
        else:
            break

    cap.release()
    return True


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_path', nargs=1, help='Path to video')
    parser.add_argument('save_path', nargs=1, help='Path to save video')
    parser.add_argument('-s', '--score', default=0.9, type=float, 
        help='Set this flag to set minimal score. Default=0.9(90%)')
    args = parser.parse_args()
    video_path = args.video_path[0]
    save_path = args.save_path[0]
    score = args.score
    
    print('Started...')
    succes = detect_on_video(video_path, save_path, score)
    if succes:
        print('Done!')
        sys.exit(0)
    else:
        print('Error')
        sys.exit(1)
    


if __name__=='__main__':
    run()
