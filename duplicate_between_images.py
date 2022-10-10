import numpy as np
import os
import concurrent.futures
import faiss
import time
import shutil
import imagehash
from PIL import Image
def dupfinder(x):
#     print("In Dupfinder")
    query = x[0]
    ref_embeddings1 = x[1]
    d = 64
    k = 1
    index = faiss.IndexBinaryFlat(d * 8)
    index.add(ref_embeddings1)
    D, I = index.search(query, k)  # sanity check
    print(D[0][0])

    if D[0][0] == 0:
#         print("Duplicate - Dupfinder")
        folder_name = "flags"
        folder_source = "img_code/"
        folder_path = os.path.join(folder_source, folder_name, "1")
        os.makedirs(folder_path)
    else:
#         print("Not Duplicate - Dupfinder")
        folder_name = "flags"
        folder_source = "img_code/"
        folder_path = os.path.join(folder_source, folder_name, "0")
        os.makedirs(folder_path)

        

new_index_type = np.empty([0, 64], dtype='uint8')
new_index_name = "img_code/embeddings/index0.npy"
np.save(new_index_name, new_index_type)

### Generating phash value in binary for Given Image
from tqdm import tqdm
reffolder = 'Data Team/dataold/'
reffolderlist=os.listdir(reffolder)
queryfolder = 'Data Team/datanewdup/'
queryfolderlist= os.listdir(queryfolder)

source_path="img_code/embeddings/index0.npy"
load_file = np.load(source_path)

for im in tqdm(reffolderlist):
    fpath = reffolder+im  # Image Path
    image = Image.open(fpath)
    phash = str(imagehash.phash(image))  # Phash value for Image
    phash_binary = str(bin(int('1' + phash, 16))[3:])  # Converting phash value to binary format
    phash_binary = [int(s) for s in phash_binary]
    phash_binary = np.array(phash_binary, dtype=np.uint8)
    phash_binary.shape = (1, 64)
    load_file = np.append(load_file, phash_binary, axis=0)
    np.save(source_path, load_file)
 
ref = np.load('img_code/embeddings/index0.npy')
print('len of ref',ref.shape)
for im2 in tqdm(queryfolderlist):
    
    fpath = queryfolder+im2 # Image Path
    print(fpath)
    image = Image.open(fpath)
    phash = str(imagehash.phash(image))  # Phash value for Image
    phash_binary = str(bin(int('1' + phash, 16))[3:])  # Converting phash value to binary format
    phash_binary = [int(s) for s in phash_binary]
    phash_binary = np.array(phash_binary, dtype=np.uint8)
    phash_binary.shape = (1, 64)
    dupfinder([phash_binary,ref])
#     print("CHECK")
    flags = os.listdir("img_code/flags")
    if "1" in flags:
        print("Duplicate Image")
#         print(fpath)
        shutil.rmtree("img_code/flags")
#         print(fpath)
        shutil.move(fpath,'duplicate_img/')
    else:
        print("Unique Image")
        shutil.rmtree("img_code/flags")
