import os
import sys
import UCFileAndDirectoryNames as info
import UserNetworkFilesGenerator as ufg


def get_all_directory_list(dir_name):
    """
    :param dir_name: Relative Path of the directory which contains the input subdirectories which contain input json files which contains the tweet
    objects.
    :return: A list of directory names which are present in the directory.
    """
    all_dir_contents = os.listdir(dir_name)
    subdirs = []
    for contents in all_dir_contents:
        if os.path.isdir(dir_name + contents):
            subdirs.append(contents)
    return subdirs



def traverse_base_input_dir(base_input_dir_name, base_output_dir_name, file_name, individual_file_flag):
    """
    :param base_input_dir_name: Directory which contains subdirectory corresponding to the directories in which the files containing information about the tweets from which the user dictionary will be generated. These subdirectories correspond contain files corresponding to a particular misninformation spread.
    :param base_output_dir_name: Directory which will contain subdirectories in which the output files containing the network will be generated
    :param file_name: The file name for the file which will contain the follower friend network for all users. This file name will be used to denote the entire network and will be used in each output subdirectory.
    :param individual_file_flag: 1 if want individual follower friend network files for each user also.
    :return: N/A
    Creates a directory which contain further subdirectories (each corresponding to the subdirectories present in the base input directory) with CSV file(s) that contain the data about the follower friend network.
    The format of the file is :
        user_1, user2 where user_1 --> user_2 (user_1 follows user_2)
    """
    subdir_list = get_all_directory_list(base_input_dir_name)
    for subdir in subdir_list:
        ufg.main(base_input_dir_name + subdir + "/", base_output_dir_name + subdir + "/", file_name, individual_file_flag)


def main(base_input_dir_name, base_output_dir_name, file_name, individual_file_flag):
    """
    :param base_input_dir_name: Directory which contains subdirectory corresponding to the directories in which the files containing information about the tweets from which the user dictionary will be generated. These subdirectories correspond contain files corresponding to a particular misninformation spread.
    :param base_output_dir_name: Directory which will contain subdirectories in which the output files containing the network will be generated
    :param file_name: The file name for the file which will contain the follower friend network for all users. This file name will be used to denote the entire network and will be used in each output subdirectory.
    :param individual_file_flag: 1 if want individual follower friend network files for each user also.
    :return: N/A
    Creates a directory which contain further subdirectories (each corresponding to the subdirectories present in the base input directory) with CSV file(s) that contain the data about the follower friend network.
    The format of the file is :
        user_1, user2 where user_1 --> user_2 (user_1 follows user_2)
    """
    if not os.path.exists(base_input_dir_name):
        print("Input Directory does not exist", base_input_dir_name)
        exit(-1)

    if not os.path.exists(base_output_dir_name):
        print("Output Directory does not exist. Making new base output directory", base_output_dir_name)
        os.makedirs(base_output_dir_name)

    traverse_base_input_dir(base_input_dir_name, base_output_dir_name, file_name, individual_file_flag)


if __name__ == '__main__':
    if len(sys.argv) == 5:
        main(sys.argv[-4], sys.argv[-3], sys.argv[-2], int(sys.argv[-1]))
    else:
        main(info.UserInformationGeneratorDirName, info.UserFilesGeneratorDirName, info.UserFilesGeneratorFileName, 0)