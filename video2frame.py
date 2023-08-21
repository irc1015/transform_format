import cv2
import argparse
from pathlib import Path
import os
import shutil
from tqdm import tqdm


def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='', help='video path')
    parser.add_argument('--second', type=float, default=3.0, help='how many seconds 1 frame')
    return parser.parse_known_args()[0] if known else parser.parse_args()

def make_frames(opt):
    path = opt.path
    second = opt.second

    video = cv2.VideoCapture(path)
    frames_num = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    print('Frames: {}'.format(frames_num))
    fps_num = int(video.get(cv2.CAP_PROP_FPS))
    print('FPS: {}'.format(fps_num))

    video_file_name = path.split('/')[-1]
    video_name = video_file_name.split('.')[0]#get video name

    #create location folder
    if os.path.exists(video_name):
        shutil.rmtree(video_name)
    Path(video_name).mkdir(parents=True, exist_ok=False)

    interval = int(fps_num * second)#every interval FPS frame extra 1 frame
    print('Every {} FPS extra 1 frame'.format(interval))
    count = 0 #compute how many frames are extraed

    #success = True

    for i in tqdm(range(frames_num)):
        success, frame = video.read()
        if success and (i == 0 or ((i + 1) % interval == 0)):
            cv2.imwrite(os.path.join(video_name, '{}.jpg'.format(count)), frame)
            count += 1
        elif not success:
            break
    print('Extra {} frames'.format(count + 1))

if __name__ == '__main__':
    opt = parse_opt()
    make_frames(opt)