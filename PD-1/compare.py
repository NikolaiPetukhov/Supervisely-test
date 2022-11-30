import argparse
import image_slicer

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('images_paths', nargs=2)
    args = parser.parse_args()
    path_A = args.images_paths[0]
    path_B = args.images_paths[1]
    if image_slicer.compare(path_A, path_B):
        print('Identical')
    else:
        print('Different')

if __name__ == "__main__":
    run()