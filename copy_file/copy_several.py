from pathlib import Path
import os
import shutil
import glob
from shutil import copy
from tqdm import tqdm

file_lst = os.listdir('/hy-tmp/noclean')
if '.DS_Store' in file_lst:
    file_lst.remove('.DS_Store')

dataset_path = '/hy-tmp/dataset_zhu'
if os.path.exists(os.path.join(dataset_path, 'images')):
    shutil.rmtree(os.path.join(dataset_path, 'images'))
Path(os.path.join(dataset_path, 'images')).mkdir(parents=True, exist_ok=False)

if os.path.exists(os.path.join(dataset_path, 'labels')):
    shutil.rmtree(os.path.join(dataset_path, 'labels'))
Path(os.path.join(dataset_path, 'labels')).mkdir(parents=True, exist_ok=False)

for file in file_lst:
    file_ = os.path.join('/hy-tmp/noclean', file)
    images_lst = os.listdir(os.path.join(file_, 'images'))
    labels_lst = os.listdir(os.path.join(file_, 'labels'))
    if '.DS_Store' in images_lst:
        images_lst.remove('.DS_Store')
    if '.DS_Store' in labels_lst:
        labels_lst.remove('.DS_Store')
    if 'classes.txt' in labels_lst:
        labels_lst.remove('classes.txt')
    if len(images_lst) == len(labels_lst):
        for i in tqdm(range(len(images_lst))):
            copy(os.path.join(file_ + '/images', images_lst[i]), os.path.join(dataset_path, 'images'))
            copy(os.path.join(file_ + '/labels', labels_lst[i]), os.path.join(dataset_path, 'labels'))
    else:
        for i in tqdm(range(len(labels_lst))):
            name = labels_lst[i][:-4] + '.jpg'
            if name in images_lst:
                index = images_lst.index(name)
                copy(os.path.join(file_ + '/images', images_lst[index]), os.path.join(dataset_path, 'images'))
            copy(os.path.join(file_ + '/images', images_lst[i]), os.path.join(dataset_path, 'labels'))



end_img = os.listdir(os.path.join(dataset_path, 'images'))
end_lab = os.listdir(os.path.join(dataset_path, 'labels'))
print('images: ' + str(len(end_img)))
print('labels: ' + str(len(end_lab)))
