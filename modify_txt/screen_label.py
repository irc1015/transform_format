import os
from tqdm import tqdm

labels_path = '/Users/zhuzhirui/Desktop/TC_dataset/labels'
images_path = '/Users/zhuzhirui/Desktop/TC_dataset/images'
DELETE_CLASS = 2
txt_lst = os.listdir(labels_path)
print(len(txt_lst))

# need delete NO.2 dog class
count = 0 #how many files have been modified
flag = False #whether this file has been modified

for i in tqdm(range(len(txt_lst))):
    with open(os.path.join(labels_path, txt_lst[i]), 'r') as f:
        lines = f.readlines()  # read all of lines in a txt file
        delete_index = []  # need delete line index
        for index in range(len(lines)):
            label = int(lines[index].split(' ')[0])  # '0 0.39453125 0.3875 0.01484375 0.0234375\n'

            if label == DELETE_CLASS:
                delete_index.append(index)
                flag = True

        if flag == True:
            count += 1
            flag = False

        new_lines = [j for i, j in enumerate(lines) if i not in delete_index]  # accord list
    f.close()

    os.remove(os.path.join(labels_path, txt_lst[i]))

    #if label txt file is empty, do not recover txt file
    #And should delete corresponding image file
    if len(new_lines) == 0:
        image_path = os.path.join(images_path, txt_lst[i][:-4] + '.jpg')
        os.remove(image_path)
    else:
        f = open(os.path.join(labels_path, txt_lst[i]), 'w')
        for item in new_lines:
            f.write(item)  # re-write
        f.close()

print('modify {} files'.format(count))
labels_length = os.listdir(labels_path)
images_length = os.listdir(images_path)
print('There are {} labels'.format(len(labels_length)))
print('There are {} images'.format(len(images_length)))
