import os
import platform

root = os.getcwd()

list = []

for subdir, dirs, files in os.walk(root):
    for file in files:
        list.append(os.path.join(subdir, file))
        #print(os.path.join(subdir, file))
length = len(list)
count = 0
for each in list:
    print("["+count+"] "+)
