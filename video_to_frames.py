# Importing all necessary libraries
import cv2
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# ffmpeg_extract_subclip("full.mp4", start_seconds, end_seconds, targetname="cut.mp4")
ffmpeg_extract_subclip("path_to_video.mp4", 0, 100, targetname="cut1.mp4")
