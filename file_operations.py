#read files to list line by line
with open(filename) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
#get list of all files recursively
import os
allfiles = [os.path.join(root,f) for root,dirs,files in os.walk('path to folder') for f in files] #https://stackoverflow.com/a/13051819

#change all yolo labels class number
headlabels=os.listdir('label folderpath')
for i in headlabels:
    print(i)
    f=open('label folderpath'+i,'r')
    lb=f.readlines()
    # print(lb)
    f.close()
    newlb=['1'+j[1:] for j in lb ]
    # print(newlb)
    write=open('label folderpath'+i,'w')
    write.writelines(newlb)
    write.close()
