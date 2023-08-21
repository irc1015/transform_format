import cv2
import argparse
from pathlib import Path
import os
import shutil
from tqdm import tqdm

def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='', help='frames folder')
    parser.add_argument('--width', type=int, default=1280, help='resize frame height')
    parser.add_argument('--height', type=int, default=720, help='resize frame width')
    return parser.parse_known_args()[0] if known else parser.parse_args()

def crop_frame(opt):
    path = opt.path
    height = opt.height
    width = opt.width

    frames_lst = os.listdir(path)
    frames_lst.sort()
    print('Original frames: {}'.format(len(frames_lst)))

    croped_path = path + '_croped'
    if os.path.exists(croped_path):
        shutil.rmtree(croped_path)
    Path(croped_path).mkdir(parents=True, exist_ok=False)

    count = 0

    for i in tqdm(range(len(frames_lst))):
        img = cv2.imread(os.path.join(path, frames_lst[i]))
        ori_height = img.shape[0]#img.shape is (h, w, c)
        ori_width = img.shape[1]

        #because lower right
        new_width = int(ori_width / 6 * 2)
        crop_img = img[(ori_height - height): , new_width:(new_width + width)]
        cv2.imwrite(os.path.join(croped_path, frames_lst[i]), crop_img)
        count += 1
    print('Croped {} frames'.format(count))

if __name__ == '__main__':
    opt = parse_opt()
    crop_frame(opt)
