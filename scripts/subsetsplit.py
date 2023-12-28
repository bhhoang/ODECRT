import os
import math
import numpy as np
from shutil import copyfile
from tqdm import tqdm
from typing import List

# List of alphanumeric characters as labels
labels: List[str] = [str(d) for d in range(10)] + [chr(d) for d in range(ord('A'), ord('Z')+1)] + [chr(d) for d in range(ord('a'), ord('z')+1)]

def copy_images(src_base: str, dest_base: str, img_nos: List[int], char_folder: str, type: str) -> None:
    """
    Copies a set of images from the source directory to the destination directory.

    Args:
    src_base (str): Base source directory path.
    dest_base (str): Base destination directory path.
    img_nos (List[int]): List of image numbers to be copied.
    char_folder (str): Specific character folder name.
    type (str): train, test, or valid.
    """
    for img_no in tqdm(img_nos, desc=f'Copying {type} for character {labels[int(char_folder)-1]}', leave=True):
        try:
            src = f"{src_base}{char_folder}/img{char_folder}-{str(img_no).zfill(5)}.png"
            dest = f"{dest_base}Sample{char_folder}/img{char_folder}-{str(img_no).zfill(5)}.png"
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            copyfile(src, dest)
        except:
            continue

def subsetsplit(base_src: str, base_dest: str, train_ratio: float = 0.80, valid_ratio: float = 0.15) -> None:
    """
    Splits the dataset into training, validation, and testing sets and copies the images to respective directories.

    Args:
    base_src (str): Base source directory path.
    base_dest (str): Base destination directory path.
    train_ratio (float): Proportion of the dataset to include in the train split (default is 0.80).
    valid_ratio (float): Proportion of the dataset to include in the validation split (default is 0.15).
    """
    for char in range(1, 63):
        char_folder = str(char).zfill(3)
        classLen = len(os.listdir(base_src + char_folder))

        trainLen = math.floor(classLen * train_ratio)
        validLen = math.ceil(classLen * valid_ratio)

        rand = np.random.randint(low=1, high=classLen + 1, size=classLen)
        randTrain = rand[:trainLen]
        randValid = rand[trainLen:trainLen + validLen]
        randTest = rand[trainLen + validLen:]

        copy_images(base_src, os.path.join(base_dest, 'train/'), randTrain, char_folder, 'train')
        copy_images(base_src, os.path.join(base_dest, 'valid/'), randValid, char_folder, 'valid')
        copy_images(base_src, os.path.join(base_dest, 'test/'), randTest, char_folder, 'test')

        #print(f'Finished processing character {char_folder}')
