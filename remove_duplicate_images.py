from os.path import join
import sys, hashlib, os, imghdr
import utils

if __name__ == '__main__':
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))
    if len(sys.argv) < 2:
        print ("Arg #1: output folder")
        sys.exit("Looks like you did not specify the source folder")        
        
    data_src = sys.argv[1]
    only_folders = utils.get_folder_list(data_src)
    folder_num = len(only_folders)
    counter = 0
    removed_files_num = 0
    for folder in only_folders:
        counter += 1
        print(counter, "/", folder_num, " current folder: ", folder)
        current_files = utils.get_file_list(join(data_src, folder))
        folder_file_num = len(current_files)
        print("Number of files in the folder: ", folder_file_num)

        to_be_removed = []
        hash_keys = dict()
        for index, filename in enumerate(current_files):                    
            current_file = join(data_src, folder, filename)
            if not os.path.isfile(current_file):
                continue

            valid_image = utils.is_image_not_corrupted(current_file)
            if not valid_image:
                to_be_removed.append(current_file)
                continue

            with open(current_file, 'rb') as f:
                filehash = hashlib.md5(f.read()).hexdigest()
            
            if filehash not in hash_keys: 
                hash_keys[filehash] = index
            else:
                to_be_removed.append(current_file)

        print("Need to remove ", len(to_be_removed), " out of ", folder_file_num)
        for filename in to_be_removed:
            utils.remove_file(filename)
            removed_files_num += 1
        
        print("")
        print("")

    print("")
    print("Number of removed files: ", removed_files_num)
    print("Number of processed folders: ", folder_num)