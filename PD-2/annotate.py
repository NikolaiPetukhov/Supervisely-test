import numpy as np
import cv2 as cv


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
    cv.rectangle(img, bbox[:2], bbox[2:4], color, 1)
    text_coordinates = (bbox[0]+1, bbox[1]+1)
    draw_text(img, text, text_coordinates, font, font_scale, color, 1, (0,0,0))

def draw_mask(img, segmentation, color):
    segments = []
    for segment in segmentation:
        segments.append([[segment[i], segment[i+1]] for i in range(0, len(segment), 2)])

    for segment in segments:
        pts = np.array(segment, np.int32)
        pts = pts.reshape((-1,1,2))
        cv.polylines(img, [pts], True, color)
        mask = img.copy()
        cv.fillPoly(mask, [pts], color)
        alpha = 0.3
        img = cv.addWeighted(mask, alpha, img, 1 - alpha, 0)
        return img


def annotate(image, image_info, image_annotations, categories, show_bbox=True, show_mask=True):
    """
    Adds annotations to an image
    Returns new image with added annotations
    """
    img = image
    image_height = image_info.get('height', 720)
    image_width = image_info.get('width', 720)
    min_font_scale = image_height/1200
    max_font_scale = image_height/400
    for annotation in image_annotations:
        if annotation.get('iscrowd', False):
            continue
        category = categories.get(annotation.get('category_id', -1), None)
        if category is None:
            continue
        bbox = annotation.get('bbox', [])
        bbox = (int(bbox[0]), int(bbox[1]), int(bbox[0])+int(bbox[2]), int(bbox[1])+int(bbox[3]))
        color = annotation.get('color', (255,255,255))
        color = (color[2], color[1], color[0])
        probability = annotation.get('probability', 1)
        text = f"{category.get('name', 'Uknown')} {int(probability*100)}%"

        annotation_area = annotation.get('area', 0)
        ratio = annotation_area / (image_height*image_width)

        font_scale = min_font_scale + (max_font_scale-min_font_scale)*min(0.2, ratio)*5
        
        # draw mask
        if show_mask:
            img = draw_mask(img, annotation.get('segmentation', [[]]), color)

        # draw bbox
        if show_bbox:
            draw_bbox(img, bbox, text, color, cv.FONT_HERSHEY_SIMPLEX, font_scale)
        
    return img
