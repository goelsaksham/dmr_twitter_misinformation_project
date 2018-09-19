import os
import json
import sys
import shutil
from functools import reduce
import FileAndDirectoryNames as info


def check_source_tweet(tweet_json):
    return tweet_json['text'].find("RT") != 0


def check_retweet_tweet(tweet_json):
    return tweet_json['text'].find("RT") == 0


def get_retweet_count(tweet_json):
    return tweet_json['retweet_count']


def retweet_count_check_gt(tweet_json, threshold_of_retweets=info.Threshold_Of_Num_Of_Retweets):
    return get_retweet_count(tweet_json) > threshold_of_retweets


def retweet_count_check_lte(tweet_json, threshold_of_retweets=info.Threshold_Of_Num_Of_Retweets):
    return (get_retweet_count(tweet_json) > 0) and \
           (get_retweet_count(tweet_json) <= threshold_of_retweets)


def retweet_count_check_eq_0(tweet_json, threshold_of_rewteets=0):
    return get_retweet_count(tweet_json) == threshold_of_rewteets


def resolve_boolean_functions(tweet_json, function_list):
    """
    :param tweet_json: Tweet Object
    :param function_list: A list of functions serving as a predicate.
    :return: Returns the final boolean which represents whether the tweet object passes the predicate of each function
    """
    return reduce(lambda accum, function : function(tweet_json) and accum, function_list, True)


def append_tweet_to_tweet_list(tweet_list, tweet_json, function_list):
    """
    :param tweet_list: List of tweet objects
    :param tweet_json: Tweet object
    :param function_list: List of functions that serve as a predicate
    :return: Appends the tweet object to the tweet_list if the tweet object satisfy each function predicate as
    present in the list of functions.
    """
    if resolve_boolean_functions(tweet_json, function_list):
        tweet_list.append(tweet_json)


def file_type_check(file_name, file_ext = info.Tweet_Output_File_Format):
    """
    :param file_name: The name of the file
    :param file_ext: The type of extension needed for the file
    :return: Checks whether the file is of the correct extension.s
    """
    return file_name.split(".")[-1] == file_ext[1:]


def get_all_files_list(dir_path):
    """
    :param dir_path: The relative path to the directory.
    :return: A list of files (not directories) which are of type json present in the directory.
    """
    all_dir_contents = os.listdir(dir_path)
    tweet_files = []
    for contents in all_dir_contents:
        if not os.path.isdir(dir_path + contents) and file_type_check(contents):
            tweet_files.append(dir_path + contents)
    return tweet_files


def create_tweet_list_from_each_file_in_directory(input_source_tweets_file_dir_path,
                                                  function_list):
    """
    :param input_source_tweets_file_dir_path: The directory path of the input directory which contains the input file.
    :param function_list: A list of function predicates that decide which tweets to filter from the file into the list.
    :return: A list of tweet objects from each file present in the input directory which satisfy each predicate as
    presented by each function in the list of functions passed as a parameter.
    """
    tweet_list = []
    input_files = get_all_files_list(input_source_tweets_file_dir_path)
    for file in input_files:
        with open(file, 'r') as file_reader:
            for tweet in file_reader:
                tweet_json = json.loads(tweet)
                append_tweet_to_tweet_list(tweet_list, tweet_json, function_list)
    return tweet_list


def create_tweet_list(input_source_tweets_file_dir_path,
                      source_tweets_file_name,
                      function_list):
    """
    :param input_source_tweets_file_dir_path: The directory path of the input directory which contains the input file.
    :param source_tweets_file_name: The name of the input file which contains the tweet objects.
    :param function_list: A list of function predicates that decide which tweets to filter from the file into the list.
    :return: A list of tweet objects from the input file which satisfy each predicate as presented by each function in
    the list of functions passed as a parameter.
    """
    tweet_list = []
    with open(input_source_tweets_file_dir_path +
              source_tweets_file_name, 'r') as file_reader:
        for tweet in file_reader:
            tweet_json = json.loads(tweet)
            append_tweet_to_tweet_list(tweet_list, tweet_json, function_list)
    return tweet_list


def create_tid_to_tweet_dict(source_tweets):
    """
    :param source_tweets: List of tweet objects which correspond to source tweets.
    :return: A dictionary that maps the Tweet ID of each source tweet to the source tweet tweet object itself.
    """
    dict = {}
    for tweet in source_tweets:
        dict[int(tweet['id'])] = tweet
    return dict


def create_tid_to_retweet_list_dict(source_tweets):
    """
    :param source_tweets: List of tweet objects which correspond to source tweets.
    :return: A dictionary that maps the Tweet ID of each source tweet to a list which will eventually contain the
    tweet object corresponding to the retweet tweet's for this tweet.
    """
    dict = {}
    for tweet in source_tweets:
        dict[int(tweet['id'])] = []
    return dict


def add_retweet_to_tid_to_retweet_list_dict(source_tweet_dict, rt_tweets_list):
    """
    :param source_tweet_dict: The dictionary that maps Source Tweets' Tweet ID to List of Retweet Tweet Objects
    :param rt_tweets_list: The list of retweet tweets' tweet objects which were collected from the input file.
    :return: N/A
    Just adds the tweet object to the corresponding source tweets' list of retweet tweets' tweet objects pres
    """
    for rt_tweet in rt_tweets_list:
        try:
            source_tweet_id = int(rt_tweet['retweeted_status']['id'])
            source_tweet_dict[source_tweet_id].append(rt_tweet)
        except:
            continue


def generate_diretory_paths(output_files_dir_path,
                            base_output_dir_name,
                            threshold_of_retweets):
    """
    :param output_files_dir_path: Represents the directory in which subdirectories will be created each of which hold the relevant classified source
    and their corresponding retweet tweets
    :param base_output_dir_name: Represents the base directory name which will be used to name the subdirectories which will be created each of which
    hold the relevant classified source and their corresponding retweet tweets. The relevant information will be added to
    the base directory name when making these directories to mark clear distinction.
    :param threshold_of_retweets: Represents the number of Retweets Required for a particular tweet to as a Threshold to mark that tweet as relevant /
    important
    :return: A list of strings where each string represents the path to the subdirectories that will be created in
    the mentioned output directory.
    """
    if threshold_of_retweets != 0:
        return [output_files_dir_path + base_output_dir_name + "_gt_" + str(threshold_of_retweets) + "_rtw/",
                output_files_dir_path + base_output_dir_name + "_lte_" + str(threshold_of_retweets) + "_rtw/",
                output_files_dir_path + base_output_dir_name + "_eq_" + str(0) + "_rtw/"]
    else:
        print("Invalid Number of Threshold:", threshold_of_retweets)
        exit(-1)


def create_directories(directory_paths):
    """
    :param directory_paths: List of directory paths in which the files can be put
    :return: N/A
    Creates directories based on the paths in the list passed as the parameter.
    If some directory already exists at this path, then removes the directory and creates new directory.
    """
    for directory in directory_paths:
        if os.path.exists(directory):
            shutil.rmtree(directory)
        os.makedirs(directory)


def get_directory_according_to_tweet_rtw_count(directory_paths, retweet_list_len):
    """
    :param directory_paths: List of directory paths in which the files can be put
    :param retweet_list_len: Number of Retweets for some source tweet
    :return: The correct directory path corresponding to the number of retweets for the source tweet.
    The correct directory path is generated by comparing the number of retweets to the Threshold in the
    FileAndDirectoryNames.py file
    """
    if retweet_list_len > info.Threshold_Of_Num_Of_Retweets:
        return directory_paths[0]
    elif (retweet_list_len > 0) and \
         (retweet_list_len <= info.Threshold_Of_Num_Of_Retweets):
        return directory_paths[1]
    else:
        return directory_paths[-1]


def populate_files(directory_paths, tid_tw_dict, tid_rtw_dict):
    """
    :param directory_paths: List of directory paths in which the files can be put
    :param tid_tw_dict: The dictionary that maps Source Tweets' Tweet ID to Tweet Object
    :param tid_rtw_dict: The dictionary that maps Source Tweets' Tweet ID to List of Retweet Tweet Objects
    :return: N/A
    Creates a file (name same as the source tweet id) in the correct subdirectory (based on number of retweets
    collected) with the first line as the source tweet object and the rest of the lines as the retweet tweet objects
    """
    for tid, o_tw in tid_tw_dict.items():
        file = open(get_directory_according_to_tweet_rtw_count(directory_paths, len(tid_rtw_dict[tid])) +
                    str(tid) + info.Tweet_Output_File_Format, "w")
        file.write(json.dumps(o_tw) + "\n")
        for tweets in tid_rtw_dict[tid]:
            file.write(json.dumps(tweets) + "\n")


def read_file(input_source_tweets_file_dir_path, source_tweets_file_name,
              output_files_dir_path, base_output_dir_name,
              threshold_of_retweets, parse_full_dir):
    """
    :param input_source_tweets_file_dir_path: Represents the relative path to the directory which contains the input file (tweets.json - created using the Search
    API script). Used in the Source and Retweet Tweet Generator Script to to load the file contents.
    :param source_tweets_file_name: Represents the name of the input file (tweets.json - created using the Search
    API script). Used in the Source and Retweet Tweet Generator Script to to load the file contents.
    :param output_files_dir_path: Represents the directory in which subdirectories will be created each of which hold the relevant classified source
    and their corresponding retweet tweets
    :param base_output_dir_name: Represents the base directory name which will be used to name the subdirectories which will be created each of which
    hold the relevant classified source and their corresponding retweet tweets. The relevant information will be added to
    the base directory name when making these directories to mark clear distinction.
    :param threshold_of_retweets: Represents the number of Retweets Required for a particular tweet to as a Threshold to mark that tweet as relevant /
    important
    :param parse_full_dir: A boolean used to tell whether to parse each and every json file in the above mentioned
    directory (1st param) to extract information or use a specific file which is specified above (2nd param)
    :return: N/A
    Is responsible to actually create the individual files for each source tweet (first line) along with retweets of that particular source tweet
    (after the first line) in the corresponding directory based on the number of retweets collected.
    """
    directory_paths = generate_diretory_paths(output_files_dir_path,
                                              base_output_dir_name,
                                              threshold_of_retweets)
    create_directories(directory_paths)

    if parse_full_dir:
        source_tweets = create_tweet_list_from_each_file_in_directory(input_source_tweets_file_dir_path,
                                                                      [check_source_tweet])
        retweet_tweets = create_tweet_list_from_each_file_in_directory(input_source_tweets_file_dir_path,
                                                                       [check_retweet_tweet])
    else:
        source_tweets = create_tweet_list(input_source_tweets_file_dir_path,
                                          source_tweets_file_name,
                                          [check_source_tweet])
        retweet_tweets = create_tweet_list(input_source_tweets_file_dir_path,
                                      source_tweets_file_name,
                                      [check_retweet_tweet])

    source_tid_to_tweet_dict = create_tid_to_tweet_dict(source_tweets)
    source_tid_to_retweet_list_dict = create_tid_to_retweet_list_dict(source_tweets)
    add_retweet_to_tid_to_retweet_list_dict(source_tid_to_retweet_list_dict, retweet_tweets)

    populate_files(directory_paths, source_tid_to_tweet_dict, source_tid_to_retweet_list_dict)


def main(input_source_tweets_file_dir_path, source_tweets_file_name,
         output_files_dir_path, base_output_dir_name,
         threshold_of_retweets, parse_full_dir):
    read_file(input_source_tweets_file_dir_path, source_tweets_file_name,
              output_files_dir_path, base_output_dir_name,
              threshold_of_retweets, parse_full_dir)


if __name__ == '__main__':
    if len(sys.argv) == 6:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[-1]), False)
    else:
        main(info.Source_Retweet_Classifier_Input_Dir_Path,
             info.Source_Retweet_Classifier_Input_File_Name,
             info.Source_Retweet_Classifier_Output_Dir_Path,
             info.Source_Retweet_Classifier_Output_Base_Dir_Name,
             info.Threshold_Of_Num_Of_Retweets,
             info.Parse_Source_Retweet_Classifier_Input_Dir)