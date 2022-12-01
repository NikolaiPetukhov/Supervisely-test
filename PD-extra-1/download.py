import argparse
from pytube import YouTube
from transformers.utils.hub import sys


def download(url, dir=None, res='720p', mime_type='video/mp4', new_name=None):
    yt = YouTube(url)
    yt = yt.streams.filter(res=res, mime_type=mime_type).first()
    yt.download(dir, new_name)
    return True


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs=1, help='YouTube video url')
    parser.add_argument('-d', '--dir', required=False, help='Directory path to save video')
    parser.add_argument('-n', '--name', required=False, help='Filename of video')
    parser.add_argument('-r', '--res', default='720p', help='Video resolution')
    args = parser.parse_args()
    url = args.url[0]
    dir = args.dir
    name = args.name
    res = args.res

    print('Downloading...')
    succes = download(url, dir=dir, res=res, new_name=name)
    if succes:
        print('Done!')
        sys.exit(0)
    else:
        print('Error')
        sys.exit(1)


if __name__=='__main__':
    run()
    