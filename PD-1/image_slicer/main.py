import os
from PIL import Image
from pathlib import Path


def _calculate_pixels(size_str: str, max_length: int):
    if size_str[-1] == "%":
        if int(size_str[:-1]) <= 0:
            raise ValueError('Length must be higher than 0')
        return min(int(size_str[:-1])*max_length//100, max_length)
    else:
        if int(size_str) <= 0:
            raise ValueError('Length must be higher than 0')
        return min(int(size_str), max_length)

def split(img_path: str, window_height: str, window_width: str, offset_x: str, offset_y: str, save_path=None):
    """
    Reads an image by given path and slices it with sliding window approach.
    Saves resulting images in the save_path directory, if save_path is None,
    then saves images in the same directory in subdirectory named like image.
    Names of saved images looks like h-w-x-y-r-c, where:
    h - resulting image height
    w - resulting image width
    x - offset by x-axis in pixels
    y - offset by y-axis in pixels
    r - row
    c - column
    You can specify window size and offsets in format <1-100>% or integer string.
    """
    path = Path(img_path)
    image = Image.open(path)
    dir_path = os.path.dirname(path)
    file_name = '.'.join(path.name.split('.')[:-1])
    file_ext = path.name.split('.')[-1]
    if save_path is None:
        save_path = f'{dir_path}/{file_name}'
    
    image_width, image_height = image.size
    window_height_px = _calculate_pixels(window_height, image_height)
    window_width_px = _calculate_pixels(window_width, image_width)
    offset_x_px = _calculate_pixels(offset_x, image_width)
    offset_y_px = _calculate_pixels(offset_y, image_height)
    if (offset_x_px > window_width_px) or (offset_y_px > window_height_px):
        raise ValueError("Offset cannot be bigger than window")
    
    window_coord = [0, 0]
    window_row = 1
    window_col = 1
    while window_coord[1] < image_height:
        tile_image = image.crop((window_coord[0], window_coord[1], 
            min(window_coord[0]+window_width_px, image_width), 
            min(window_coord[1]+window_height_px, image_height)))
        if not os.path.exists(f"{save_path}"):
            os.makedirs(f"{save_path}")
        tile_image.save(f"{save_path}/{image_height}-{image_width}-{offset_x_px}-" +
            f"{offset_y_px}-{window_row}-{window_col}.{file_ext}")
        window_coord[0] = window_coord[0] + offset_x_px
        window_col += 1
        if window_coord[0] >= image_width:
            window_coord[0] = 0
            window_col = 1
            window_coord[1] = window_coord[1] + offset_y_px
            window_row += 1
    
def compare(path_A: str, path_B: str):
    """
    Reads 2 images by given paths and compares them. Images are considered indentical
    if its sizes are equal and all pixels are same
    """
    image_A = Image.open(path_A)
    image_B = Image.open(path_B)
    return _compare_images(image_A, image_B)

def _compare_images(image_A: Image, image_B: Image):
    size_A = image_A.size
    size_B = image_B.size
    if not size_A == size_B:
        return False 
    pixels_A = list(image_A.getdata())
    pixels_B = list(image_B.getdata())
    return pixels_A == pixels_B

def merge(path: str, save_path: str):
    """
    Reads all images in given path, merges them into one and saves it under save_path.
    All images should be named like "h-w-x-y-r-c", where:
    h - resulting image height
    w - resulting image width
    x - offset by x-axis in pixels
    y - offset by y-axis in pixels
    r - row
    c - column
    """
    newImage = None
    for dir_entry in os.scandir(Path(path)):
        if dir_entry.is_file():
            filename = dir_entry.name
            file_path = dir_entry.path
            try: 
                image = Image.open(file_path)
            except:
                continue
            ih, iw, ox, oy, r, c = (int(x) for x in filename.split('.')[0].split('-'))
            if newImage is None:
                newImage = Image.new(image.mode, (iw, ih))
            newImage.paste(image, (ox*(c-1), oy*(r-1)))
    if not newImage is None:
        newImage.save(f"{save_path}")
