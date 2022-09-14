#read files to list line by line
with open(filename) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
#get list of all files recursively
import os
allfiles = [os.path.join(root,f) for root,dirs,files in os.walk('path to folder') for f in files]
