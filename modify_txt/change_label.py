import os
from tqdm import tqdm

labels_path = '/hy-tmp/TC_dataset/labels'
'''original:
        0: car
        1: dog
        2: person
   now:
        0: person
        1: car
        2: dog'''

txt_lst = os.listdir(labels_path)
print(len(txt_lst))

for i in tqdm(range(len(txt_lst))):
    with open(os.path.join(labels_path, txt_lst[i]), 'r') as f:
        lines = f.readlines()  # read all of lines in a txt file
        new_lines = []  # need delete line index
        for index in range(len(lines)):
            label = int(lines[index].split(' ')[0])  # '0 0.39453125 0.3875 0.01484375 0.0234375\n'

            if label == 0:
                new_str = '1' + ''.join(lines[index][1:])
            elif label == 1:
                new_str = '2' + ''.join(lines[index][1:])
            else:
                new_str = '0' + ''.join(lines[index][1:])

            new_lines.append(new_str)
    f.close()

    os.remove(os.path.join(labels_path, txt_lst[i]))

    f = open(os.path.join(labels_path, txt_lst[i]), 'w')
    for item in new_lines:
        f.write(item)
    f.close()
