from os import listdir, mkdir
from os.path import isfile, isdir, join
import sys
from shutil import copyfile

TRAIN_DIR_NAME = "train"
TEST_DIR_NAME = "test"
SPLIT_RATIO = 20

def get_file_list(data_location):
    return  [f for f in listdir(data_location) if isfile(join(data_location, f))]

def get_folder_list(data_location):
    return [f for f in listdir(data_location) if isdir(join(data_location, f))]

def copy_files(file_list, src, dst):
    for single_file in file_list:
        print("Copying ", join(src, single_file), " to ", join(dst, single_file))
        copyfile(join(src, single_file), join(dst, single_file))

if __name__ == '__main__':
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))
    if len(sys.argv) <= 2:
        print ("Arg #1: input folder")
        print ("Arg #2: output folder")
        sys.exit("Looks like you did not specify the location of your data")        
        
    data_src = sys.argv[1]
    data_output = sys.argv[2]

    only_folders = get_folder_list(data_src)
    print(only_folders)
    mkdir(data_output)
    mkdir(join(data_output, TRAIN_DIR_NAME))
    mkdir(join(data_output, TEST_DIR_NAME))
    for folder in only_folders:
        
        current_files = get_file_list(join(data_src, folder))
        class_size = len(current_files)
        test_size = int(round((class_size/100)*SPLIT_RATIO))
        train_size = class_size - test_size

        print(join(data_src, folder), ", size = ", class_size, ", test = ", test_size, ", train = ", train_size)
        print(len(current_files[:test_size]))
        print(len(current_files[test_size:]))
        current_train_folder = join(data_output, TRAIN_DIR_NAME, folder)
        current_test_folder = join(data_output, TEST_DIR_NAME, folder)
        mkdir(current_train_folder)
        mkdir(current_test_folder)
        copy_files(current_files[:test_size], join(data_src, folder), current_test_folder)
        copy_files(current_files[test_size:], join(data_src, folder), current_train_folder)
        