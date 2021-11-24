import os
from PIL import Image

#list of files
path = '../media/face/'
file_list = os.listdir(path)
print(file_list)

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)

#create directory
for i in file_list:
    new_path = './Face/' + i[:7]
    createFolder(new_path + '/')

new_path = './Face/'
folder_list = os.listdir(new_path)
print(folder_list)


cnt = 0
for i in file_list:
    cnt += 1
    data_path = new_path + i[:7] + '/'
    for j in folder_list:
        if i[:7] == j:
            os.replace(path, data_path + i[:7] + '_' + str(cnt) + '.jpg')