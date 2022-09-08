import mediapipe as mp
import cv2
image=cv2.imread("path to image")
mp_face_detection = mp.solutions.face_detection
# Prepare DrawingSpec for drawing the face landmarks later.
mp_drawing = mp.solutions.drawing_utils 
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
face_detection=mp_face_detection.FaceDetection(min_detection_confidence=0.5, model_selection=0)
results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
