import os
import shutil
from typing import List
import glob
import xml.etree.ElementTree as ET
from tqdm import tqdm
from pathlib import Path

def delete_DS(path:str) -> List[int]:
    filelst = os.listdir(path)
    if '.DS_Store' in filelst:
        filelst.remove('.DS_Store')
    return filelst

class_names = ['roadnonclean',]

save_path = '/Users/zhuzhirui/Desktop/tc/labels'
if os.path.exists(save_path):
    shutil.rmtree(save_path)
Path(save_path).mkdir(parents=True, exist_ok=False)

def single_xml2txt(xml_file:str):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    txt_file = xml_file.split('.')[0] + '.txt'
    txt_name = txt_file.split('/')[-1]
    txt_path = os.path.join(save_path, txt_name)

    with open(txt_path, 'w') as txt_path:
        for member in root.findall('object'):
            class_name = member[0].text  # [name, pose, truncated, difficult, bndbox]
            if class_name in class_names:
                class_num = class_names.index(class_name)  # index of classnames list
                picture_width = int(root.find('size')[0].text) #[width, height, depth]
                picture_height = int(root.find('size')[1].text)

                box_x_min = int(member[4][0].text)#bndbox -> [xmin, ymin, xmax, ymax]
                box_y_min = int(member[4][1].text)
                box_x_max = int(member[4][2].text)
                box_y_max = int(member[4][3].text)

                x_center = (box_x_min + box_x_max) / (2 * picture_width)
                y_center = (box_y_min + box_y_max) / (2 * picture_height)
                width = (box_x_max - box_x_min) / (2 * picture_width)
                height = (box_y_max - box_y_min) / (2 * picture_height)

                txt_path.write(str(class_num) + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(width) + ' ' + str(height) + '\n')

def dir_xml2txt(path:str):
    xml_lst = glob.glob(os.path.join(path, '*.xml'))
    for xml_file in tqdm(xml_lst):
        single_xml2txt(xml_file)

path = '/Users/zhuzhirui/Desktop/城管项目相关文档/道路不洁'
dir_xml2txt(path)

images_lst = glob.glob(os.path.join(path, '*.jpg'), recursive=True)
images_path = '/Users/zhuzhirui/Desktop/tc/images'
if os.path.exists(images_path):
    shutil.rmtree(images_path)
Path(images_path).mkdir(parents=True, exist_ok=False)

for image in images_lst:
    shutil.copy(image, images_path)

end_img = os.listdir(os.path.join('/Users/zhuzhirui/Desktop/tc', 'images'))
end_lab = os.listdir(os.path.join('/Users/zhuzhirui/Desktop/tc', 'labels'))
print('images: ' + str(len(end_img)))
print('labels: ' + str(len(end_lab)))
