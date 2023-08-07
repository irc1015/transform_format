import argparse
from pathlib import Path
import os
import random
from shutil import copy
from tqdm import tqdm

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', type=str , default='have_test', help='no_test/have_test')
    parser.add_argument('--path', type=str, default='/home/irccc/桌面/BDD100K', help='dataset path')
    parser.add_argument('--new_path', type=str, default='/home/irccc/PycharmProjects/BDD100K', help='new dataset path')
    parser.add_argument('--train_rate', type=float, default=0.7, help='train dataset rate')
    parser.add_argument('--val_rate', type=float, default=0.6, help='val dataset rate')
    parser.add_argument('--have_mask', default=True, help='whether objective detection or not')

    return parser.parse_known_args()[0] if known else parser.parse_args()
    #namespace, extra = parser.parse_known_args()


def handle(opt):
    mode = opt.mode
    path = str(opt.path)
    new_path = str(opt.new_path)
    train_rate = opt.train_rate
    have_mask = opt.have_mask

    if mode == 'have_test':
        val_rate = opt.val_rate

        os.makedirs(os.path.join(new_path, 'train'), exist_ok=True)
        os.makedirs(os.path.join(os.path.join(new_path, 'train'), 'image'), exist_ok=True)
        os.makedirs(os.path.join(os.path.join(new_path, 'train'), 'label'), exist_ok=True)

        os.makedirs(os.path.join(new_path, 'val'), exist_ok=True)
        os.makedirs(os.path.join(os.path.join(new_path, 'val'), 'image'), exist_ok=True)
        os.makedirs(os.path.join(os.path.join(new_path, 'val'), 'label'), exist_ok=True)

        os.makedirs(os.path.join(new_path, 'test'), exist_ok=True)
        os.makedirs(os.path.join(os.path.join(new_path, 'test'), 'image'), exist_ok=True)
        os.makedirs(os.path.join(os.path.join(new_path, 'test'), 'label'), exist_ok=True)

        image_path = Path(path + '/image')
        image = os.listdir(image_path)
        image.sort()
        #print('original images are {}'.format(len(image)))

        if have_mask == True:
            label_path = Path(path + '/label')
            label = os.listdir(label_path)
            label.sort()
            #print('original labels are {}'.format(len(label)))

            merge = list(zip(image, label))
            random.shuffle(merge)
            image, label = zip(*merge)

            train_len = int(len(image) * train_rate)

            train_image = image[:train_len]
            other_image = image[train_len:]
            train_label = label[:train_len]
            other_label = label[train_len:]

            for i in tqdm(range(train_len)):
                copy(os.path.join(path + '/image', train_image[i]), os.path.join(new_path + '/train', 'image'))
                copy(os.path.join(path + '/label', train_label[i]), os.path.join(new_path + '/train', 'label'))

            val_len = int(len(other_image)*val_rate)
            val_image = other_image[:val_len]
            val_label = other_label[:val_len]

            test_image = other_image[val_len:]
            test_label = other_label[val_len:]

            for i in tqdm(range(val_len)):
                copy(os.path.join(path + '/image', val_image[i]), os.path.join(new_path + '/val', 'image'))
                copy(os.path.join(path + '/label', val_label[i]), os.path.join(new_path + '/val', 'label'))


            for i in tqdm(range(len(test_image))):
                copy(os.path.join(path + '/image', test_image[i]), os.path.join(new_path + '/test', 'image'))
                copy(os.path.join(path + '/label', test_label[i]), os.path.join(new_path + '/test', 'label'))


    elif mode == 'no_test':
        val_rate = 1 - train_rate


if __name__ == '__main__':
    opt = parse_opt()
    handle(opt)