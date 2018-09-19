from GenerateNetworkGraph import GraphNodesNeighbors
import json
from datetime import datetime
import operator
import os
import re


def sortedUserTimeStamps(jsonFile):
    if not os.path.isdir(jsonFile):
        with open(jsonFile,'r') as f:
            ID_timestampDict = {}
            for tweet in f:
                tweet_json = json.loads(tweet)
                user_id = int(tweet_json['user']['id'])
                timestamp = str(tweet_json['created_at'])
                ID_timestampDict[user_id] = datetime.strptime(timestamp, "%a %b %d %H:%M:%S %z %Y")

            return [a for a, b in sorted(ID_timestampDict.items(), key=operator.itemgetter(1))], ID_timestampDict
    else:
        return [], None


JSONDir = "../../Tweets_Collection/data/relevant_tweets/Rumor11/"

graph = GraphNodesNeighbors("../../User_Collection/data/user_graph_files/Rumor11/follower_friend_graph.csv")
graph.construct_graph()

allJSONs = os.listdir(JSONDir)

for JSON in allJSONs:
    print("Processing : "+ JSON)
    (sortedIDs, tstampDictionary) = sortedUserTimeStamps(JSONDir  + JSON)

    if sortedIDs != []:
        userFollows = []

        for idx in range(1,len(sortedIDs)):
            currUser = sortedIDs[idx]
            prevUsers = set(sortedIDs[0:idx])
            influencers = prevUsers.intersection(graph.get_user_friends(currUser))

            for influencer in influencers:
                userFollows.append((influencer, currUser, tstampDictionary.get(currUser).strftime("%x %X")))

        pattern = re.compile("[\[\]\(\)]")
        with open("../out_data/InfectionSpreadGraph.csv","a+") as f:
            for user in userFollows:
                f.write(re.sub(pattern, "", str(user)))
                f.write("\n")
