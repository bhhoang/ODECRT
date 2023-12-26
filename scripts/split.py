import os
import shutil
from sklearn.model_selection import train_test_split
import numpy as np
import random
from subsetsplit import subsetsplit
# Create label map
labelMap = [str(d) for d in range(0,10)] + [chr(d) for d in range(ord('A'), ord('Z')+1)] + [chr(d) for d in range(ord('a'), ord('z')+1)]

# Directory of the dataset
baseGood = '../English/Img/GoodImg/Bmp/'
baseBad = '../English/Img/BadImag/Bmp/'
gooDataDirectory = os.listdir(baseGood)
baDataDirectory = os.listdir(baseBad)
destDirectory = os.path.join('../dataset/')

if not os.path.isdir(destDirectory):
    os.mkdir(destDirectory)
if not os.path.isdir(f'{destDirectory}train'):
    os.mkdir(f'{destDirectory}train')
if not os.path.isdir(f'{destDirectory}valid'):
    os.mkdir(f'{destDirectory}valid')
if not os.path.isdir(f'{destDirectory}test'):
    os.mkdir(f'{destDirectory}test')

totalDataDirectory = gooDataDirectory + baDataDirectory

for i in sorted(totalDataDirectory):
    if not os.path.isdir(f'{destDirectory}train/{i}'):
        os.mkdir(f'{destDirectory}train/{i}')
    if not os.path.isdir(f'{destDirectory}valid/{i}'):
        os.mkdir(f'{destDirectory}valid/{i}')
    if not os.path.isdir(f'{destDirectory}test/{i}'):
        os.mkdir(f'{destDirectory}test/{i}')

subsetsplit(f'{baseGood}Sample', destDirectory)
subsetsplit(f'{baseBad}Sample', destDirectory)