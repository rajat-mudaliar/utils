import json
import os
#load empty json file
jsonfile=os.listdir("annotation_json_person_male_female")
person_cats={'male':0,'female':1}
for jsonfilename in jsonfile:
#jsonfilename=jsonfile[15]
	print(jsonfilename)
	with open('annotation_json_person_male_female/'+jsonfilename) as f:
	    alljson = json.load(f)
	    f.close()
	#### Start process
	count_files_new = 0  
	image_size = 1280
	region_ids = {'head':0}
	count_files = len(alljson['_via_img_metadata'].keys())
	#print("total files",count_files)

	import cv2
	import shutil
	count_files_new = 0  
	fold=''
	image_folder_path='images/Combined_Images/'
	for (image_id, attr) in alljson['_via_img_metadata'].items():
		filename = image_id.split(".",1)[0]
		yolo_img_out = os.path.join("yolo_person_manual_annotation", fold, 'images')
		yolo_label_out = os.path.join("yolo_person_manual_annotation",fold, 'labels')
		if not os.path.exists(yolo_img_out):
			os.makedirs(yolo_img_out)
		if not os.path.exists(yolo_label_out):
			os.makedirs(yolo_label_out)

		img_cats = []
		#print(image_folder_path+image_id.split(".",1)[0]+'.jpg')
		img=cv2.imread(os.path.join(image_folder_path,image_id.split(".",1)[0]+'.jpg'))
		img_height=img.shape[0]
		img_width=img.shape[1]
		for lb in attr['regions']:
			cat=lb['region_attributes']['crowd_person']
			#         print(lb)
			x=int(lb['shape_attributes']["x"])
			y=int(lb['shape_attributes']["y"])
			width=int(lb['shape_attributes']["width"])
			height=int(lb['shape_attributes']["height"])
			h_ratio = image_size / img_height
			w_ratio = image_size / img_width
			x= x * w_ratio
			y = y * h_ratio
			width= width * w_ratio
			height = height * h_ratio
			x_center = ( x + (width / 2) ) /  image_size  #normalized
			y_center = (y + (height / 2) ) / image_size   #normalized
			width = width  / image_size                    #normalized
			height = height / image_size                  # normalized

			try:
				catnum=person_cats[cat]
				label_filename = os.path.join(yolo_label_out, filename + ".txt")
				#print(label_filename)
				out_string = str(catnum) + " " + str(x_center) + " " + str(y_center) + " " + str(width) + " " + str(height) + "\n"
				with open(label_filename, 'a') as file1:
					file1.write(out_string)
					print('written',filename)
				shutil.copy(os.path.join(image_folder_path,filename+'.jpg'),yolo_img_out)
				count_files_new+=1

			except:
				#print("key not in this category")
				continue
	print(jsonfilename, count_files_new)
