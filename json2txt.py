import os
import json
from tqdm import tqdm
import cv2
import argparse

TRAIN_LABEL_NAME = "bdd100k_labels_images_train.json"
VAL_LABEL_NAME = "bdd100k_labels_images_val.json"
MAX_SAMPLES = 10000

classes = ["person", "bike", "car", "motor", "bus", "truck", "rider", "train"]

counter = {} #count how many objectives of every class in whole dataset

for c in classes:
    counter[c] = 0
#{'person': 0, 'bike': 0, 'car': 0, 'motor': 0, 'bus': 0, 'truck': 0, 'rider': 0, 'train': 0} initional counter

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--images_path', type=str, default='/Users/zhuzhirui/Desktop/BDD100K/image')
    parser.add_argument('--labels_path', type=str, default='/Users/zhuzhirui/Desktop/BDD100K/label')
    return parser.parse_args()

def convert(image_name, label):
    img = cv2.imread(image_name)
    width, height = img.shape[1], img.shape[0]
    dw = 1.0 / width
    dh = 1.0 / height

    catName = label['category']
    classIndex = classes.index(catName)
    roi = label['box2d']

    w = roi['x2'] - roi['x1']
    h = roi['y2'] - roi['y1']
    x_center = roi['x1'] + w/2
    y_center = roi['y1'] + h/2

    x_center, y_center, w, h = x_center * dw, y_center * dh, w * dw, h * dh
    return "{} {} {} {} {}\n".format(classIndex, x_center, y_center, w, h)



if __name__ == '__main__':
    args = get_args()
    image_Root_Path = args.images_path
    label_File_Path = [os.path.join(args.labels_path, TRAIN_LABEL_NAME), os.path.join(args.labels_path, VAL_LABEL_NAME)]

    image_name_list = os.listdir(image_Root_Path)
    print("Original samples are {}".format(len(image_name_list)))

    lines = [] #read all of labels json files information
    for label_file in label_File_Path:
        with open(label_file) as file:
            one_line = json.load(file)#read a label json file information
            lines.extend(one_line)#merge into lines
            print("label {}".format(label_file))

    for line in tqdm(lines):
        name = line['name']
        labels = line['labels']
        imagePath = os.path.join(image_Root_Path, name)

        labelfilename = name[:-4] + '.txt' #label files used in YOLO is .txt format
        labelPath = os.path.join(args.labels_path, labelfilename)

        if not os.path.isfile(os.path.realpath(imagePath)):
            continue #image file name which is in label files, but can not find in images folder

        with open(labelPath, 'w') as file:
            for label in labels:
                cat = label['category']
                if cat in classes:
                    counter[cat] += 1
                    file.write(convert(imagePath, label))
        #When a label txt file has been written, mark this image in folder
        image_index = image_name_list.index(name)
        image_name_list[image_index] = 'done'
    print(counter)

    #When all of label txt files have been output finally, check which images have been marked
    #then remove them
    for image in image_name_list:
        if image != 'done':
            os.remove(os.path.join(image_Root_Path, image))
    image_name_list = os.listdir(image_Root_Path)
    print("Now samples are {}".format(len(image_name_list)))