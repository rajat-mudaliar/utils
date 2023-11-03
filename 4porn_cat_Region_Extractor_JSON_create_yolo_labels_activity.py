import json
import os
import numpy as np
import cv2

__auther__ = "Abhishek"

users = [ "shyam", "old40k", "prashant" , "mohit", "vinay" ]
#"akash"

for user in users:
  json_fold = os.path.join('porncat/json_data_manual_annotation/', user)
  jsonfiles = os.listdir(json_fold)
  for json_file in jsonfiles:
    print(json_file)
    # image_data_path = os.path.join('porncat/newdata/')
    image_data_path = os.path.join('/data/ajay/yolo_porn_data/0complete_merged_data/new_merged_data/')
    #if user == "old40k":
    #  image_data_path = os.path.join('/data/docker/test20/yolov5/porncat/final_clean_data/combined/')
    json_path = os.path.join(json_fold, json_file)

    image_size = 640
    '''
    cats = ['kissing', 'Kissing', 'Sexual_Intimacy', 'Sexual_intimacy', 'sexual_intimacy', "anal fingering", 'Anal Fingering', 'breast_pressing', 'Breast_Pressing','Breast_pressing', 'Breast_Sucking ', 'Breast_Sucking', 'breast_sucking', 'Breast_Sucking',  'Breast_sucking', 'Footjob', 'Hand_job_to_boy', 'hand_job_to_boy', 'hand_job_to_girl', 'Mammary sex', 'Toy_Sex', 'Tribadism', 'Cunnilingus', 'fellatio','Fellatio','Annilingus ',"Analingus","Anilingus","annilingus","Annilingus","anallingus", 'Anal_Penetration', "anal_penetration", 'Male_female_penetration',  'male_female_penetration', 'Anus_Torture', 'BDSM', 'Body_Torture', 'Breast_Torture', 'Collared', 'Face_Torture', 'Foot_leg_Torture', 'Hand_arm_Torture', 'Penis_Torture', 'Vulva_Torture', 'anus_torture']
    
    cats = sorted(list(set([cat.lower() for cat in cats])))
    print(cats)

    cats = ['anal fingering', 'anal_penetration', 'annilingus', 'anus_torture', 'bdsm', 'body_torture', 'breast_pressing', 'breast_torture', 'collared', 'cunnilingus', 'face_torture', 'fellatio', 'foot_leg_torture', 'footjob', 'hand_arm_torture', 'hand_job_to_boy', 'hand_job_to_girl', 'kissing', 'male_female_penetration', 'mammary_sex', 'penis_torture', 'sexual_intimacy', 'toy_sex', 'tribadism', 'vulva_torture'] 
    ''' 

  
    # sexual region id s

    #region_ids = {'male_female_penetration':'0', 'fellatio':'1','kissing':'2','hand_job_to_boy':'3','hand_job_to_girl':'4',
    #              'Toy_Sex':'5','Anal_Penetration':'6', 'Cunnilingus':'7', 'Anilingus':'7', 'female_masturbation':'5', 
    #              'breast_sucking':'8', "breast_pressing":'9', 'Sexual_Intimacy':'10', "sexual_intimacy":"10",
    #              "Anal Fingering":'11', "Footjob":"12", "Mammary sex":"13", "Tribadism":"14", "Cum shot":"15",         
    #              "BDSM":"16", "Breast_Torture":"17", "Vulva_Torture":"18", "Penis_Torture":"19", "Face_Torture":"20", "Collared":"21", 
    #              "Hand_arm_Torture":"22", "Foot_leg_Torture":"23", "Body_Torture":"24"}
                  
    region_ids = {'male_female_penetration':'0', 'fellatio':'1','kissing':'2','hand_job_to_boy':'3','hand_job_to_girl':'4',
                  'toy_sex':'5','anal_penetration':'6', 'cunnilingus':'7', 'annilingus':'7', 'breast_sucking':'8', "breast_pressing":'9', 
                  "sexual_intimacy":"10", "anal fingering":'11', "footjob":"12", "mammary_sex":"13", "tribadism":"14", 'anus_torture':'15',         
                  "bdsm":"16", "breast_torture":"17", "vulva_torture":"18", "penis_torture":"19", "face_torture":"20", "collared":"21", 
                  "hand_arm_torture":"22", "foot_leg_torture":"23", "body_torture":"24"}

    cats=[]
    for keyc in region_ids.keys():
      cats.append(keyc)

    with open(json_path) as file:
        # print(json_path)
        json_data = json.load(file)
        via_img_metadata = json_data['_via_img_metadata']
        
    count_files = 0
    flag_dict = {}
    for (image_id, attr) in via_img_metadata.items():
      if flag_dict.get(image_id,0)==0:   
        count_files += 1      
    
    
    #### Start process
    count_files_new = 0    
    flag_dict = {}
    for (image_id, attr) in via_img_metadata.items():

      if flag_dict.get(image_id,0)==0:   flag_dict[image_id]=1;
      filename = attr['filename']
      
      ### Select train_val folder
      count_files_new += 1
      if count_files_new < int(0.85 * count_files):
        fold = "training"
      else:
        fold = "val"
        
      yolo_img_out = os.path.join(f"porncat/training_testing_yolo/cats", fold, 'images')
      yolo_label_out = os.path.join(f"porncat/training_testing_yolo/cats",fold, 'labels')
 
      if not os.path.exists(yolo_img_out):
        os.makedirs(yolo_img_out)
      if not os.path.exists(yolo_label_out):
        os.makedirs(yolo_label_out)
    
      # Reading image and converting to RGB if not
      '''
      image_path = os.path.join(image_data_path, filename)
      print(image_path)
      image = cv2.imread(image_path)  # for invalid_image path function returns none
      print(image.shape)
      image = np.array(image)
      '''
      try:
        image_path = os.path.join(image_data_path, filename)
        image = cv2.imread(image_path)   # for invalid_image path function returns none
        image = np.array(image)
      except (IOError, ValueError, IndexError) as e:
        # print('{}: {}'.format(image_path, e))
        pass
      else:
        if image.ndim<2:
          print('Bad_image...........', json_path+"/"+filename)
          continue
        elif image.ndim==2:
          image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGB)
          # print('Dimension of RGB converted image: {}'.format(image.ndim))

      regions = attr['regions']
      img_cats = []
      for i,reg in enumerate(regions):
        shape_attributes = reg['shape_attributes']
        region_attributes = reg['region_attributes']

        # extracting only rectangle shapes
        if shape_attributes['name']=='rect':
          x = shape_attributes['x']
          y = shape_attributes['y']
          width = shape_attributes['width']
          height = shape_attributes['height']

          img_height, img_width, channels = image.shape
          resized_image = cv2.resize(image, (image_size, image_size), interpolation=cv2.INTER_NEAREST)

          #resized height, width, x, y
          h_ratio = image_size / img_height
          w_ratio = image_size / img_width

          x= x * w_ratio
          y = y * h_ratio
          width= width * w_ratio
          height = height * h_ratio

          #img_region = resized_image[int(y):int(y+height), int(x):int(x+width), :]
          if img_region.size==0:
            continue
          #img_region_scaled = cv2.resize(img_region, (224,224))

          x_center = ( x + (width / 2) ) / image_size  #normalized
          y_center = (y + (height / 2) ) / image_size   #normalized
          width = width  / image_size                    #normalized
          height = height / image_size                  # normalized

          #image_filename = os.path.join(yolo_img_out, filename)
          sexual_regions = region_attributes['sexual_regions']
          region_category = list(sexual_regions.keys())
          for reg1 in region_category:
            if sexual_regions[reg1] == True:
              img_cats.append(reg1)
          
          img_cats = list(set([cat.lower() for cat in img_cats])) 
          
          img_cats = ["anal_fingering" if cat in ["anal fingering", 'Anal Fingering'] else cat for cat in img_cats]
          img_cats = ["mammary_sex" if cat in ["mammary sex"] else cat for cat in img_cats]     
          img_cats = ["annilingus" if cat in ['analingus', 'anallingus', 'anilingus', 'annilingus', 'annilingus '] else cat for cat in img_cats]         
          img_cats = ['breast_sucking' if cat in ['breast_sucking', 'breast_sucking '] else cat for cat in img_cats]
          
          img_cats = sorted(list(set([cat.lower() for cat in img_cats])))             

          
          for cat in img_cats:
            #try:
            label_filename = os.path.join(yolo_label_out, filename[0:-4] + ".txt")
            # class x_center y_center width height
            if cat in cats:
                out_string = str(region_ids[cat]) + " " + str(x_center) + " " + str(y_center) + " " + str(width) + " " + str(height) + "\n"
                with open(label_filename, 'a') as file1:
                  file1.write(out_string)

                if not os.path.exists(yolo_img_out + "/" +filename):
                    cv2.imwrite(yolo_img_out + '/' +filename, resized_image )
                    pass
                    

