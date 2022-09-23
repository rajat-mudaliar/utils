import json
import os
import glob

import cv2
import pdb

import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-labels", help="labels for which via json is to be created")
parser.add_argument("-images", help="path to PornCat inference output directory")
parser.add_argument("-outfolder", help="path to PornCat inference output directory")

args = parser.parse_args()
 
labels = args.labels
# cats_exp = args.cats

# assert "labels" not in cats_exp, "Please pass dir path till 'exp' only e.g. runs/detect/exp11"


#part_no = 4

#part_name = f"bdsm_part{part_no}"
part_images = os.listdir(f"{labels}")

filename_wo_extension = [os.path.splitext(fname)[0] for fname in part_images]

text_files_path0 = labels #  os.path.join(cats_exp, "labels")                             # porncat

img_files_path = args.images
text_files = glob.glob(text_files_path0+"/*.txt")

print("Text files all: ", len(text_files), "\n", text_files[:5])

part_text_files = []
for path in text_files:
    # name_only = os.path.splitext(os.path.basename(path))[0]
    # if name_only in filename_wo_extension:
        part_text_files.append(path)

print("Text files after taking from parts: ", len(part_text_files), "\n", part_text_files[2500:2550])
#exit(0)

via_json_file_path = './sample_blank.json'

data_dict = {}
'''
catergory_list = {0:'male_female_penetration', 1:'fellatio', 2:'kissing', 3:'hand_job_to_boy', 4:'hand_job_to_girl',
                  5:'Toy_Sex', 6:'Anal_Penetration', 7:'Cunnilingus', 8:'penis', 9:'breasts', 10:'Buttocks', 11:'vulva',
                  12:'boy_in_underwear', 13:'girl_in_underwear', 14:'Partial_Buttocks', 15:'Partial_Breasts',
                  16:'Breasts_in_Bra', 17:'face'}
'''                  
catergory_list={0:'male',1:'female'}

via_json_data = {}
with open(via_json_file_path, 'r') as f:
    via_json_data = json.load(f)

_via_img_metadata = via_json_data['_via_img_metadata']


for txt_f in part_text_files:
    filename_with_ext = os.path.basename(txt_f)
    filename = filename_with_ext.split('.')[0]
    print("Filename:", filename)

    # cat, x_centre, y_centre, width, height = None, None, None, None, None

    pred_results = []
    with open(txt_f, 'r') as f:
        line = f.readline()
        while line:
            parts = [float(i)  for i in line.split()]
            #print(len(parts))
            pred_results.append(parts)  # [ cat x_cen y_cen width height ]
            line = f.readline() # reading next line

    img_path = os.path.join(img_files_path, filename + ".jpg")
    if not os.path.exists(img_path):
        print(f"{img_path} imagefile doesn't exists....")
        continue

    img_filename_with_ext = os.path.basename(img_path)
    file_disk_size = os.path.getsize(img_path)
    img_ndarray = cv2.imread(img_path)
    img_height, img_width = img_ndarray.shape[:2]
    print("Image Dimension:", img_height, " x ", img_width)

    regions = []
    for result in pred_results:
        cat, x_cen, y_cen, width, height  = result[:5]
        # cat, x_cen, y_cen, height, width = result
        width = width*img_width
        height = height*img_height
        box_x = x_cen*img_width - width/2
        box_y = y_cen*img_height - height/2

        cat_name = catergory_list[int(result[0])]
        print(cat_name)
        regions.append({
            "shape_attributes": {
                    "name": "rect",
                    "x": int(box_x),
                    'y': int(box_y),
                    'width': int(width),
                    'height': int(height)
            },
            "region_attributes": {
                "crowd_person": cat_name
            }
        })
    print("Region list:\n", regions)
    file_anno_info = _via_img_metadata.get(img_filename_with_ext, None)
    if file_anno_info is None:
        _via_img_metadata[img_filename_with_ext] = {
            "filename": img_filename_with_ext ,
            "size": file_disk_size,
            "regions": regions,
            "file_attributes": {
            }
        }
    else:
        regions_present = file_anno_info['regions']
        regions_present.extend(regions)
        
        #file_anno_info['regions'] = regions_present
        #pdb.set_trace()


#via_json_data['_via_img_metadata'] = {}

with open(args.outfolder+'.json', 'w') as f:
    json.dump(via_json_data, f)
    





