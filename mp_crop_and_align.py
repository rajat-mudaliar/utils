import cv2
import numpy as np
import insightface.utils.face_align
#import mediapipe and create mesh object
import mediapipe as mp
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    refine_landmarks=True,
    max_num_faces=2,
    min_detection_confidence=0.5)
#function to align the face
def mpal(results,image):
  lm=results.multi_face_landmarks[0]
  mleft,mright,eleft,eright,nose=[],[],[],[],[]

  for lnum in [291,292,306,307,308, 324,325,318,319,320,324,325,407]:
    mright.append([int(lm.landmark[lnum].x * image.shape[1]),int(lm.landmark[lnum].y * image.shape[0])])
  mouth_right = np.mean(mright, axis=0)
  mouth_right=[int(i) for i in mouth_right]

  for lnum in [61,62,76,77,78,88,89,90,95, 146, 183]:
    mleft.append([int(lm.landmark[lnum].x * image.shape[1]),int(lm.landmark[lnum].y * image.shape[0])])
  mouth_left = np.mean(mleft, axis=0)
  mouth_left=[int(i) for i in mouth_left]

  for lnum in [33,246,161,160,159,158,157,173,133,155,145,144,163,7]:
    eleft.append([int(lm.landmark[lnum].x * image.shape[1]),int(lm.landmark[lnum].y * image.shape[0])])
  eye_left=[int(i) for i in np.mean(eleft, axis=0)]

  for lnum in [362,384,385,386,387,388,466,263,249,390,373,374,380,381,382]:
    eright.append([int(lm.landmark[lnum].x * image.shape[1]),int(lm.landmark[lnum].y * image.shape[0])])
  eye_right=[int(i) for i in np.mean(eright, axis=0)]

  for lnum in [4,1,275,274,44]:
    nose.append([int(lm.landmark[lnum].x * image.shape[1]),int(lm.landmark[lnum].y * image.shape[0])])
  nose_point=[int(i) for i in np.mean(nose, axis=0)]
  kps=np.array([eye_left,eye_right,nose_point,mouth_left,mouth_right])
  aimg = face_align.norm_crop(image, kps)
  return aimg

results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

if results.multi_face_landmarks == None :
  print('no face detected')
if results.multi_face_landmarks:
  print('face detected')
  if len(results.multi_face_landmarks) == 1:
    face=mpal(results,image)#face contains cropped and aligned face array
