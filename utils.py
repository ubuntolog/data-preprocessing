from os import listdir, mkdir, remove
from os.path import isfile, isdir, join, exists
from shutil import copyfile
from PIL import Image

ALLOWED_IMAGE_FORMATS = ["jpg", "jpeg", "png"]

def get_file_list(data_location):
    return  [f for f in listdir(data_location) if isfile(join(data_location, f))]

def get_folder_list(data_location):
    return [f for f in listdir(data_location) if isdir(join(data_location, f))]

def copy_files(file_list, src, dst):
    for single_file in file_list:
        print("Copying ", join(src, single_file), " to ", join(dst, single_file))
        copyfile(join(src, single_file), join(dst, single_file))

def remove_file(file_name):
    if exists(file_name):
        remove(file_name)
    else:
        print("Cannot remove the file: ", file_name)


def has_valid_image_format(file_name):
    valid_image = False

    for extension in ALLOWED_IMAGE_FORMATS:
        if file_name.lower().endswith(extension):
            valid_image = True
            break

    return valid_image


def is_image_not_corrupted(file_name, debug=False):    
    if has_valid_image_format(file_name):
        try:
            img = Image.open(file_name)
            img.verify()
            return True
        except (IOError, SyntaxError) as e:
            if debug:
                print(e)
                print("Possibly corrupted image file: ", file_name)
    return False