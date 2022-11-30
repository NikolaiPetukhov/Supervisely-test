import argparse
from merge_videos import merge

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('videos_path', nargs=1, help='Path to video directory')
    parser.add_argument('save_path', nargs=1, help='Path to save video')
    parser.add_argument('-r', '--ratio', default='16:9', 
        help='dimensions ratio of resulting video')
    args = parser.parse_args()
    videos_path = args.videos_path[0]
    save_path = args.save_path[0]
    ratio = args.ratio
    print('Merging...')
    merge(videos_path, save_path, ratio)
    print('Done!')
    

if __name__ == "__main__":
    run()