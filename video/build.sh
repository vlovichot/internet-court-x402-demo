#!/bin/bash
set -e
A=assets; W=/tmp/clips; mkdir -p $W
mk() { # name frames dir fostart
  local z; if [ "$3" = "1" ]; then z="1+0.07*on/$2"; else z="1.07-0.07*on/$2"; fi
  ffmpeg -y -v error -i $A/$1.png -vf "scale=1408:792:force_original_aspect_ratio=increase,crop=1408:792,zoompan=z='$z':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$2:s=1280x720:fps=30,fade=t=in:st=0:d=0.4,fade=t=out:st=$4:d=0.4" -c:v libx264 -pix_fmt yuv420p -r 30 $W/$1.mp4
}
mk s1-title   135 1 4.1
mk s2-pages   150 0 4.6
mk s3-terminal 165 1 5.1
mk s4-studio  150 0 4.6
mk s5-release 165 1 5.1
mk s6-refund  165 0 5.1
mk s7-closing 150 1 4.6
for s in s1-title s2-pages s3-terminal s4-studio s5-release s6-refund s7-closing; do echo "file '$s.mp4'"; done > $W/list.txt
ffmpeg -y -v error -f concat -safe 0 -i $W/list.txt -c copy $W/video.mp4
ffmpeg -y -v error -i $W/video.mp4 -i $A/narration.mp3 -filter_complex "[1:a]adelay=1500|1500,apad,atrim=0:36,loudnorm[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k court402-demo.mp4
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 court402-demo.mp4
