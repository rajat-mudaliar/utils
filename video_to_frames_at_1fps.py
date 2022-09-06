import os
import cv2
import moviepy.editor

#set rate for frames per second
def getFrames(vid, output, rate=1, frameName='frame'):
    vidcap = cv2.VideoCapture(vid)
    clip = moviepy.editor.VideoFileClip(vid)

    seconds = clip.duration
    print('durration: ' + str(seconds))
    
    count = 0
    frame = 0
    
    if not os.path.isdir(output):
        os.mkdir(output)
    
    success = True
    while success:
        vidcap.set(cv2.CAP_PROP_POS_MSEC,frame*1000)      
        success,image = vidcap.read()

        ## Stop when last frame is identified
        print(frame)
        if frame > seconds or not success:
            break

        print('extracting frame ' + frameName + '-%d.png' % count)
        name = output + '/' + frameName + '-%d.png' % count # save frame as PNG file
        cv2.imwrite(name, image)
        frame += rate
        count += 1
getFrames("/home/gpu1/rajat/CrowdCounting-P2PNet/cut1.mp4","frames1")
