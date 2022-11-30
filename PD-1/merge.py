import argparse
import sys
import image_slicer

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('images_directory_path', nargs=1, help='Path to directory with images to merge')
    parser.add_argument('save_image_path', nargs=1, help='Path to save image')
    args = parser.parse_args()
    path = args.images_directory_path[0]
    save_path = args.save_image_path[0]
    try:
        print('Merging...')
        image_slicer.merge(path, save_path)
        print('Done')
    except NotADirectoryError:
        sys.exit('Not a directory')
    except Exception as e:
        sys.exit(e)


if __name__ == "__main__":
    run()