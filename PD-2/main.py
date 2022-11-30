import argparse
import json
import random
import cv2 as cv
from annotate import annotate
from matplotlib import colors

COLORS = ['blue', 'purple', 'red', 'green', 'orange', 'salmon', 'pink', 'gold',
            'orchid', 'slateblue', 'limegreen', 'seagreen', 'darkgreen', 'olive',
            'teal', 'aquamarine', 'steelblue', 'powderblue', 'dodgerblue', 'navy',
            'magenta', 'sienna', 'maroon']


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--save', required=False, help='Path where to save ' 
        'annotated image. If not present, Image wont be saved.')
    parser.add_argument('image_path', nargs=1, help='Path to an image')
    parser.add_argument('annotations_path', nargs=1, help='Path to annotations json file')
    parser.add_argument('image_id', nargs=1, help='Image id from annotations', type=int)
    args = parser.parse_args()
    image_path = args.image_path[0]
    annotations_path = args.annotations_path[0]
    save_path = args.save
    image_id = args.image_id[0]

    with open(annotations_path, 'r') as f:
        data = json.load(f)

    categories = {x.get('id', 0):x for x in data.get('categories', [])}
    print(categories)
    print()

    image_info = None
    for ii in data.get('images', []):
        if ii.get('id', None) == image_id:
            image_info = ii

    print(image_info)
    print()

    image_annotations = []
    for ia in data.get('annotations', []):
        if ia.get('image_id', None) == image_info.get('id', None):
            image_annotations.append({**ia, 
                'color': tuple(int(c*255) for c in colors.to_rgb(random.choice(COLORS))),
                'probability': (90 + random.randint(0, 9))/100
            })

    print(json.dumps(image_annotations, indent=2))
    print()

    img = cv.imread(image_path)
    img = annotate(img, image_info, image_annotations, categories)
    if save_path:
        cv.imwrite(save_path, img)

    cv.imshow('Image', img)
    cv.waitKey(0)


if __name__ == '__main__':
    run()