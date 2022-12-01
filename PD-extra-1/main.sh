#! /usr/bin/bash

python3 download.py "https://www.youtube.com/watch?v=y0r4Lhg1PrA" -d videos -n video.mp4 -r 720p
if [ $? -eq 0 ] 
then 
  echo "Video downloaded!" 
else 
  echo "Could not Download video" >&2 
  exit 1 
fi
python3 cut_video.py -f videos/video.mp4 random 50 videos/cutted.mp4
if [ $? -eq 0 ] 
then 
  echo "Video cutted!"
else 
  echo "Could not cut video" >&2 
  exit 1 
fi
python3 detect_on_video.py videos/cutted.mp4 videos/annotated.mp4
if [ $? -eq 0 ] 
then 
  echo "Video annotated!" 
  exit 0 
else 
  echo "Could not annotate" >&2 
  exit 1 
fi