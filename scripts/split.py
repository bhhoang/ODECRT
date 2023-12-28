import os
from typing import List
from subsetsplit import subsetsplit

def create_directories(base_path: str, subdirs: List[str]) -> None:
    """
    Creates specified subdirectories under a base path if they do not already exist.

    Args:
    base_path (str): The base directory path.
    subdirs (List[str]): List of subdirectory names to be created.
    """
    for subdir in subdirs:
        dir_path = os.path.join(base_path, subdir)
        os.makedirs(dir_path, exist_ok=True)

def remove_files(base_path: str, files: List[str]) -> None:
    """
    Removes specified files from a given base path.

    Args:
    base_path (str): The base directory path.
    files (List[str]): List of file paths to be removed.
    """
    for file_path in files:
        full_path = os.path.join(base_path, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            print(f"Removed file: {full_path}")
        else:
            print(f"File not found: {full_path}")

if __name__ == "__main__":
    from subsetsplit import subsetsplit

    # Label map
    labelMap: List[str] = [str(d) for d in range(10)] + [chr(d) for d in range(ord('A'), ord('Z')+1)] + [chr(d) for d in range(ord('a'), ord('z')+1)]

    # Define directoríe
    baseGood: str = '../English/Img/GoodImg/Bmp/'
    baseBad: str = '../English/Img/BadImag/Bmp/'
    destDirectory: str = '../dataset/'

    # Remove outlier images. Reference from https://github.com/mitchellvitez/chars74k
    files_to_remove: List[str] = [f'Sample053/img053-000{num}.png' for num in [49, 28, 24, 9, 35]]

    remove_files(baseGood, files_to_remove)
    create_directories(destDirectory, ['train', 'valid', 'test'])

    # Merge and sort directory listings
    totalDataDirectory: List[str] = sorted(os.listdir(baseGood) + os.listdir(baseBad))

    # dataset for train, valid, test directories
    for subdir in ['train', 'valid', 'test']:
        for char_dir in totalDataDirectory:
            create_directories(os.path.join(destDirectory, subdir), [char_dir])

    # Split datasets in to datasets for training, validation, and testing
    subsetsplit(f'{baseGood}Sample', destDirectory)
    subsetsplit(f'{baseBad}Sample', destDirectory)
