import os
import sys
import json
import UCFileAndDirectoryNames as info
import FollowerListGenerator as follower
import FriendListGenerator as friend


def json_type_file(file_name):
    """
    :param file_name: The name of some file
    :return: True of the extension of the file is json, False otherwise
    """
    return file_name.split(".")[-1] == "json"


def get_all_files_list(dir_name):
    """
    :param dir_name: Relative Path of the directory which contains the input json files which contains the tweet
    objects.
    :return: A list of files which are present in the directory and are of type json
    """
    all_dir_contents = os.listdir(dir_name)
    tweet_files = []
    for contents in all_dir_contents:
        if not os.path.isdir(dir_name + contents) and json_type_file(contents):
            tweet_files.append(contents)
    return tweet_files


def get_user_info_tuple(tweet_json, info_params):
    return tuple([tweet_json['user'][param] for param in info_params])


def add_to_user_info_to_dict_from_a_file(dir_name, file_name, user_info_dict, info_params):
    """
    :param dir_name: Relative Path of the directory which contains the input json files which contains the tweet
    objects.
    :param file_name: The name of the individual file which will be read to extract the information of the users and
    add them into the dictionary passed as the parameter to the function.
    :param user_info_dict: The dictionary which contains the mappings from user information to the follower and
    friend user id's list
    :param info_params: a tuple of attributes of user you want in the dictionary
    :return: N/A
    Just adds the user id's present in the input file to the dictionary. Does not add if the user id is already
    present in the dictionary.
    """
    with open(dir_name + file_name, 'r') as f:
        for tweet in f:
            tweet_json = json.loads(tweet)
            user_info = get_user_info_tuple(tweet_json, info_params)
            if not (user_info in user_info_dict):
                user_info_dict[user_info] = ([], [])


def get_all_user_id_from_directory_files(dir_name, info_params=('id',)):
    """
    :param dir_name: The directory path that contains the tweet metadata files in json format
    :param info_params: a tuple of attributes of user you want in the dictionary
    :return: A dictionary that contains information about the users aggregate from all the files present in the folder
    The dictionary has the following format:
        keys - (user_id, user_screen_name)
        values - (follower_list, friend_list)
    * here follower_list - represents the users that follow the current user (in key)
    * here friend_list - represents the users that the current user (in key) follows
    """
    user_info_dict = {}
    all_json_files = get_all_files_list(dir_name)
    for files in all_json_files:
        add_to_user_info_to_dict_from_a_file(dir_name, files, user_info_dict, info_params)
    return user_info_dict


def get_all_user_info_set_from_directory_files(dir_name, info_params=('id',)):
    """
    :param dir_name: The directory path that contains the tweet metadata files in json format
    :param info_params: a tuple of attributes of user you want in the dictionary
    :return: A dictionary that contains information about the users aggregate from all the files present in the folder
    The dictionary has the following format:
        keys - (user_id, user_screen_name)
        values - (follower_list, friend_list)
    * here follower_list - represents the users that follow the current user (in key)
    * here friend_list - represents the users that the current user (in key) follows
    """
    user_info_dict = {}
    all_json_files = get_all_files_list(dir_name)
    for files in all_json_files:
        add_to_user_info_to_dict_from_a_file(dir_name, files, user_info_dict, info_params)
    return set(user_info_dict.keys())


def main(dir_name, info_params=('id',)):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    return get_all_user_id_from_directory_files(dir_name, info_params)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[-1])
    else:
        main(info.UserInformationGeneratorDirName)