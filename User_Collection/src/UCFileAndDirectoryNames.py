"""
This file is responsible to hold the data about the different relative paths to the directories that will hold the
data and will be used to actually generate the correct data.
"""

"""
Represents the directory path (relative) of the directory that contains the file(s) (json) which contains the tweet 
objects for which the user follower and friend network needs to be generated.  
"""
UserInformationGeneratorDirName = "../../Tweets_Collection/data/relevant_tweets/"

"""
Represents the directory path (relative) of the directory in which the output file(s) should be generated
"""
UserFilesGeneratorDirName = "../data/user_graph_files/"

"""
Represents the name of the file which should be generated and will contain the information of the whole follower and 
friend network of all users collected from the input files.
"""
UserFilesGeneratorFileName = "follower_friend_graph.csv"

"""
Represents the directory path (relative) of the directory in which the output file(s) should be generated
"""
UserListFileGeneratorDirName = "../data/user_graph_files/user_list/"

"""
Represents the name of the file which should be generated and will contain the information of the whole follower and 
friend network of all users collected from the input files.
"""
UserListFileGeneratorFileName = "user_list.csv"
