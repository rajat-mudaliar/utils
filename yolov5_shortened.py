import os,detect1,torch,utils,cv2
from models.common import DetectMultiBackend
import numpy as np
from utils.datasets import  LoadImages
from utils.general import non_max_suppression,scale_coords
device= utils.torch_utils.select_device(2)
images=os.listdir('/data/rajat/csa_images_teen')
model = DetectMultiBackend('/data/integrated_code/yolo/genitals.pt', device=device, dnn=False, fp16=False)
for img_name in images:
	dataset = LoadImages('/data/rajat/csa_images_teen/'+img_name, img_size=640, stride=model.stride, auto=model.pt)
	for path, ima, im0s, vid_cap, s in dataset:
	    im,im0=ima,im0s
	im = torch.from_numpy(im).to(device)
	im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
	im /= 255  # 0 - 255 to 0.0 - 1.0
	if len(im.shape) == 3:
	    im = im[None]  # expand for batch dim
	# Inference
	pred = model(im, augment=False, visualize=False)
	pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45, classes=None,agnostic=False, max_det=1000)
	all_labels=[]
	for i, det in enumerate(pred):  # per image
	    s += '%gx%g ' % im.shape[2:]  # print string
	    if len(det):
	       det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
	for *xyxy, conf, cls in reversed(det):
	    label =  f'{model.names[int(cls)]} {conf:.2f}'
	    all_labels.append(label)
	print(all_labels)
