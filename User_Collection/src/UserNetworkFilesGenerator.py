import os
import sys
import shutil
import UCFileAndDirectoryNames as info
import UserInformationGenerator as uig
import FollowerListGenerator as follower
import FriendListGenerator as friend


def write_user_info_to_file(output_dir_name, file_name, user_info_dict):
    """
    :param output_dir_name: Name of the directory in which the output file will be generated
    :param file_name: Name of the output file which will contain the graph information
    :param user_info_dict: The dictionary which contains the relevant information about the user_ids
    :return: N/A
    Creates a file which contains the whole network of user's follower and friend network for all users present in
    the dictionary.
    The format of the file is :
        "user_1, user2" where user_1 --> user_2 (user_1 follows user_2)
    """
    with open(output_dir_name+file_name, "w") as f:
        for user_info, (follower_list, friend_list) in user_info_dict.items():
            user_id = user_info[0]

            follower_list.clear()
            follower_list += follower.generate_followers_list(user_id)
            for follower_user_id in follower_list:
                f.write(str(follower_user_id) + "," + str(user_id) + "\n")
            follower_list.clear()

            friend_list.clear()
            friend_list += friend.generate_friends_list(user_id)
            for friend_user_id in friend_list:
                f.write(str(user_id) + "," + str(friend_user_id) + "\n")
            friend_list.clear()


def create_whole_graph_file(output_dir_name, file_name, user_info_dict):
    """
    :param output_dir_name: Name of the directory in which the output file will be generated
    :param file_name: Name of the output file which will contain the graph information
    :param user_info_dict: The dictionary which contains the relevant information about the user_ids
    :return: N/A
    Creates a file which contains the whole network of user's follower and friend network for all users present in
    all the files present in the input directory.
    The format of the file is :
        "user_1, user2" where user_1 --> user_2 (user_1 follows user_2)
    """
    write_user_info_to_file(output_dir_name, file_name, user_info_dict)


def create_individual_user_graph_file(output_dir_name, file_name, user_info_dict):
    """
    :param output_dir_name: Name of the directory in which the output file will be generated
    :param file_name: Name of the output file which will contain the graph information
    :param user_info_dict: The dictionary which contains the relevant information about the user_ids
    :return: N/A
    Creates individual files for each user which contains the whole network of user's follower and friend network for
    all users present in all the files present in the input directory.
    The format of every file is :
        "user_1, user2" where user_1 --> user_2 (user_1 follows user_2)
    """
    for (user_id, user_name), (follower_list, friend_list) in user_info_dict.items():
        new_file_name = str(user_id) + ".csv"
        write_user_info_to_file(output_dir_name, new_file_name, {(user_id, user_name): (follower_list, friend_list)})


def main(input_dir_name, output_dir_name, file_name, individual_file_flag):
    """
    :param input_dir_name: Directory in which the files containing information about the tweets from which the user dictionary will be generated
    :param output_dir_name: Directory in which the files will be generated
    :param file_name: The file name for the file which will contain the follower friend network for all users
    :param individual_file_flag: 1 if want individual follower friend network files for each user also.
    :return: N/A
    Creates a directories with CSV file(s) that contain the data about the follower friend network.
    The format of the file is :
        user_1, user2 where user_1 --> user_2 (user_1 follows user_2)
    """
    if not os.path.exists(input_dir_name):
        print("Input Directory does not exist", input_dir_name)
        exit(-1)

    if os.path.exists(output_dir_name):
        shutil.rmtree(output_dir_name)

    os.makedirs(output_dir_name)

    if individual_file_flag:
        create_individual_user_graph_file(output_dir_name, file_name,
                                          uig.get_all_user_id_from_directory_files(input_dir_name))

    create_whole_graph_file(output_dir_name, file_name,
                            uig.get_all_user_id_from_directory_files(input_dir_name))


if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[-3], sys.argv[-2], int(sys.argv[-1]))
    else:
        main(info.UserInformationGeneratorDirName, info.UserFilesGeneratorDirName, info.UserFilesGeneratorFileName, 0)