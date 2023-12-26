import os
import shutil
from sklearn.model_selection import train_test_split

# Create label map
labelMap = [str(d) for d in range(0,10)] + [chr(d) for d in range(ord('A'), ord('Z')+1)] + [chr(d) for d in range(ord('a'), ord('z')+1)]

if not os.path.isdir('../dataset'):
  os.mkdir('../dataset')

if not os.path.isdir('../dataset/train'):
  os.mkdir('../dataset/train')
if not os.path.isdir('../dataset/valid'):
  os.mkdir('../dataset/valid')
if not os.path.isdir('../dataset/test'):
  os.mkdir('../dataset/test')
baseGood = '../English/Img/GoodImg/Bmp/'
baseBad = '../English/Img/BadImag/Bmp/'
gooDataDirectory = os.listdir(baseGood)
baDataDirectory = os.listdir(baseBad)

totalDataDirectory = gooDataDirectory + baDataDirectory

for i in sorted(totalDataDirectory):
    if not os.path.isdir('../dataset/train/' + i):
        os.mkdir('../dataset/train/' + i)
    if not os.path.isdir('../dataset/valid/' + i):
        os.mkdir('../dataset/valid/' + i)
    if not os.path.isdir('../dataset/test/' + i):
        os.mkdir('../dataset/test/' + i)

for i in range(1,63):
    print(f'Start spliting for character {labelMap[i-1]}, {i}/62')
    goodPath = f'{baseGood}Sample{str(i).zfill(3)}'
    badPath = f'{baseBad}Sample{str(i).zfill(3)}'
    goodData = os.listdir(goodPath)
    badData = os.listdir(badPath)
    # Add base path to each data
    goodData = [goodPath + '/' + x for x in goodData]
    badData = [badPath + '/' + x for x in badData]
    totalData = goodData + badData
    # Split data into train, valid, test
    train, test = train_test_split(totalData, test_size=0.2, random_state=42)
    train, valid = train_test_split(train, test_size=0.2, random_state=42)
    for j in range(len(train)):
        src = train[j]
        dst = '../dataset/train/' + src.split('/')[-2] + '/' + src.split('/')[-1]
        shutil.copyfile(src, dst)
    for j in range(len(valid)):
        src = valid[j]
        dst = '../dataset/valid/' + src.split('/')[-2] + '/' + src.split('/')[-1]
        shutil.copyfile(src, dst)
    for j in range(len(test)):
        src = test[j]
        dst = '../dataset/test/' + src.split('/')[-2] + '/' + src.split('/')[-1]
        shutil.copyfile(src, dst)
    print(f'Finish character {labelMap[i-1]}, {i}/62')
