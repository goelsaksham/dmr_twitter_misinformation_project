import os
import sys
import functools
import UserInformationGenerator as uig


def get_all_directory_list(dir_name):
    """
    :param dir_name: Relative Path of the directory which contains the input subdirectories which contain input json files
    which contains the tweet
    objects.
    :return: A list of directory names which are present in the directory.
    """
    all_dir_contents = os.listdir(dir_name)
    subdirs = []
    for contents in all_dir_contents:
        if os.path.isdir(dir_name + contents):
            subdirs.append(contents)
    return subdirs


def get_user_set_list_from_base_input_dir(base_input_dir_name):
    """
    :param base_input_dir_name: Directory which contains subdirectory corresponding to the directories in which the files containing information about the tweets from which the user dictionary will be generated. These subdirectories correspond contain files corresponding to a particular misninformation spread.
    :return: N/A
    Creates a directory which contain further subdirectories (each corresponding to the subdirectories present in the base input directory) with CSV file(s) that contain the data about the follower friend network.
    The format of the file is :
        user_1, user2 where user_1 --> user_2 (user_1 follows user_2)
    """
    subdir_list = get_all_directory_list(base_input_dir_name)
    list_of_user_sets = []
    for subdir in subdir_list:
        list_of_user_sets.append((subdir, uig.get_all_user_info_set_from_directory_files(base_input_dir_name + subdir + "/")))
    return list_of_user_sets


def generate_all_permutations(orig_list):
    if len(orig_list) == 0:
        return [[]]
    else:
        first_elem = orig_list[0]
        permut_1 = generate_all_permutations(orig_list[1:])
        permut_2 = []
        for elem in permut_1:
            ls = list(elem)
            ls.append(first_elem)
            permut_2.append(ls)
        return permut_1 + permut_2


def get_union_of_sets_in_list(ls):
    return functools.reduce(lambda accum, set_obj: accum | set_obj[1], ls, set({}))


def get_interesection_of_sets_in_list(ls):
    return functools.reduce(lambda accum, set_obj: accum & set_obj[1], ls, get_union_of_sets_in_list(ls))


def get_file_name_from_list(ls):
    return functools.reduce(lambda accum, set_obj: accum + "-" + str(set_obj[0]), ls, "IntersectionOfUserFiles") + \
           ".txt"


def generate_all_intersections(permut_list):
    return [(get_file_name_from_list(permut), get_interesection_of_sets_in_list(permut)) for permut in permut_list]


def filter_based_on_len(orig_list, length):
    return list(filter(lambda ls: len(ls) >= length, orig_list))


def file_writer(base_output_dir_name, tuple_obj):
    file_w = open(base_output_dir_name + tuple_obj[0], "w")
    file_w.write(str(tuple_obj[1])[1:-1].replace("(", "").replace(")", "").replace(" ", "").replace(",,", "\n"))


def generate_all_files(base_input_dir_name, base_output_dir_name):
    all_intersections = generate_all_intersections(filter_based_on_len(generate_all_permutations(
        get_user_set_list_from_base_input_dir(base_input_dir_name)), 2))
    for each_tup_object in all_intersections:
        file_writer(base_output_dir_name, each_tup_object)


def main(base_input_dir_name, base_output_dir_name):
    """
    :param base_input_dir_name: Directory which contains subdirectory corresponding to the directories in which the files containing information about the tweets from which the user dictionary will be generated. These subdirectories correspond contain files corresponding to a particular misninformation spread.
    :param base_output_dir_name: Directory which will contain subdirectories in which the output files containing the network will be generated
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

    generate_all_files(base_input_dir_name, base_output_dir_name)


if __name__ == '__main__':
    if len(sys.argv) == 4:
        main(sys.argv[-3], sys.argv[-2])
    else:
        main("../../Tweets_Collection/data/tweet_raw_json_files/", "../data/Testing/")