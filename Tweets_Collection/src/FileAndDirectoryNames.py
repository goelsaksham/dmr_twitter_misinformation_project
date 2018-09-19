"""
This file is responsible to hold the data about the different relative paths to the directories and also some other
file names that will hold the data and will be used to actually generate the correct data.
"""

"""
This variable represents the query for which you want to collect the data from twitter.
The format of the query is String List List. The outer list signifies a disjunctive form (OR)
The inner lists represents the conjunctive form (AND).
e.g. - [['I', 'am', 'Groot'], ['I', 'am', 'Steve', 'Rogers']]
Essentially This is equivalent to saying - "I AND am AND Groot OR I AND am AND Steve AND Rogers"
"""
Query_For_Tweet = [['maxine', 'waters', 'impeach', 'trump']]

"""
This variable stores the information about the file format of the type of files that should be created for storing 
the data related to the tweets.
"""
Tweet_Output_File_Format = '.json'

"""
This represents the relative path to the directory where you want to store the files containing data about the tweets 
corresponding to the query used when using the Search API Script.  
"""
Search_Tweet_Output_Directory = '../data/tweet_raw_json_files/'


"""
Represents the number of Retweets Required for a particular tweet to as a Threshold to mark that tweet as relevant / 
important
"""
Threshold_Of_Num_Of_Retweets = 100

"""
Represents the relative path to the directory which contains the input file (tweets.json - created using the Search 
API script). Used in the Source and Retweet Tweet Generator Script to to load the file contents.
"""
Source_Retweet_Classifier_Input_Dir_Path = "../data/tweet_raw_json_files/"

"""
A boolean used to tell whether to parse each and every json file in the above mentioned directory to extract 
information or use a specific file which is specified below
"""
Parse_Source_Retweet_Classifier_Input_Dir = False

"""
Represents the name of the input file (tweets.json - created using the Search
API script). Used in the Source and Retweet Tweet Generator Script to to load the file contents.
"""
Source_Retweet_Classifier_Input_File_Name = "maxine AND waters AND impeach AND trump.json"

"""
Represents the directory in which subdirectories will be created each of which hold the relevant classified source 
and their corresponding retweet tweets
"""
Source_Retweet_Classifier_Output_Dir_Path = "../data/"

"""
Represents the base directory name which will be used to name the subdirectories which will be created each of which 
hold the relevant classified source and their corresponding retweet tweets. The relevant information will be added to 
the base directory name when making these directories to mark clear distinction.
"""
Source_Retweet_Classifier_Output_Base_Dir_Name = "retweet_classifier"
