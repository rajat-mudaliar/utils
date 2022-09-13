#read files to list line by line
with open(filename) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]
