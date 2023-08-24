import os
from tqdm import tqdm

label_path = '/hy-tmp/TC_dataset/labels'
txt_lst = os.listdir(label_path)

# need delete NO.2 dog class
count = 0 #how many files have been modified
flag = False#whether this file has been modified

for i in tqdm(range(len(txt_lst))):
    with open(os.path.join(label_path, txt_lst[i]), 'r') as f:
        lines = f.readlines()  # read all of lines in a txt file
        delete_index = []  # need delete line index
        for i in range(len(lines)):
            label = int(lines[i].split(' ')[0])  # '0 0.39453125 0.3875 0.01484375 0.0234375\n'
            if label == 2:
                delete_index.append(i)
                flag = True

        if flag == True:
            count += 1
            flag = False

        new_lines = [j for i, j in enumerate(lines) if i not in delete_index]  # accord list
    f.close()

    f = open(os.path.join(label_path, txt_lst[i]), 'w')
    f.close()  # this operation can delete whole content of txt

    f = open(os.path.join(label_path, txt_lst[i]), 'w')
    for item in new_lines:
        f.write(item)#re-write 
    f.close()

print('modify {} files'.format(count))
