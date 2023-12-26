import os
import math
import numpy as np
from shutil import copyfile
from tqdm import tqdm

labels = [str(d) for d in range(0,10)] + [chr(d) for d in range(ord('A'), ord('Z')+1)] + [chr(d) for d in range(ord('a'), ord('z')+1)]

def copy_images(src_base, dest_base, img_nos, char_folder):
    for img_no in img_nos:
        src = f"{src_base}{char_folder}/img{char_folder}-{str(img_no).zfill(5)}.png"
        dest = f"{dest_base}Sample{char_folder}/img{char_folder}-{str(img_no).zfill(5)}.png"
        #print(src, dest)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        copyfile(src, dest)

def subsetsplit(base_src, base_dest, train_ratio=0.80, valid_ratio=0.15):
    for char in tqdm(range(1, 63), desc='Copying images'):
        char_folder = str(char).zfill(3)
        classLen = len(os.listdir(base_src+char_folder))

        trainLen = math.floor(classLen * train_ratio)
        validLen = math.ceil(classLen * valid_ratio)

        rand = np.random.randint(low=1, high=classLen + 1, size=classLen)
        randTrain = rand[:trainLen]
        randValid = rand[trainLen:trainLen + validLen]
        randTest = rand[trainLen + validLen:]

        copy_images(base_src, os.path.join(base_dest, 'train/'), randTrain, char_folder)
        copy_images(base_src, os.path.join(base_dest, 'valid/'), randValid, char_folder)
        copy_images(base_src, os.path.join(base_dest, 'test/'), randTest, char_folder)