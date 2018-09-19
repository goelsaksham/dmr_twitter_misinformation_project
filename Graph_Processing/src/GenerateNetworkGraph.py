"""
This file is responsible to contain two classes that generate a particular type of graph for the input file.
The two graphs differ in the way they preserve the information about the Graph.

GraphNodesEdges --> Is responsible to hold the contents of the graph in the manner as follows:
                    ({V}, {E})
                    {V} --> is a set of Vertices or Nodes (Correspond to a User)
                    {E} --> is a set of Edges where each edge is represented in form of a tuple (Node1, Node2)
                    such that Node1 --> Node2 (Node1 follows Node2)

GraphNodesNeighbors --> Is responsible  to hold the contents of the graph in the manner as follows:
                        { V1 : {N11, N12 ... } .... Vn: {Nn1, Nn2 .... } }
                        Vk --> represents a vertex or node (Correspond to a User)
                        {Nki} --> represents the neighbors. Neighbors means that Vk --> Vi
                        (User Vk follows User Vi)
"""
from functools import reduce


class GraphNodesEdges:
    """
    GraphNodesEdges -->
        Is responsible to hold the contents of the graph in the manner as follows:
        ({V}, {E}) (type: tuple) --> A tuple of two elements (Set of Vertices and Set of Edges)
        {V} (type: set) --> is a set of Vertices or Nodes (Correspond to a User Id)
        {E} (type: set) --> is a set of Edges where each edge is represented in form of a tuple (Vi, Vj)
                such that Vi --> Vj (Vi follows Vj)
    """
    def __init__(self, input_file_path: str):
        self.input_file = input_file_path
        self.users = set()
        self.edges = set()

    def get_users(self):
        return self.users

    def get_edges(self):
        return self.edges

    def get_graph(self):
        return self.get_users(), self.get_edges()

    def add_user(self, user_id: int):
        if user_id not in self.users:
            self.users.add(user_id)

    def add_user_friend(self, user_id: int, friend_id: int):
        if user_id in self.users:
            if (user_id, friend_id) not in self.edges:
                self.edges.add((user_id, friend_id))
        else:
            print("User Id not present in the Graph, User Id:", user_id)

    def add_list_data(self, ls_data: list):
        if len(ls_data) == 2:
            self.add_user(ls_data[0])
            self.add_user(ls_data[-1])
            self.add_user_friend(ls_data[0], ls_data[-1])
        else:
            print("Input data invalid. Length of the list should be 2. List:", ls_data)

    def get_num_of_users(self):
        return len(self.users)

    def get_num_of_edges(self):
        return len(self.edges)

    def get_input_file_name(self):
        return self.input_file

    def get_user_friends(self, user_id: int, user_index: int= 0):
        if user_id in self.users:
            return set(filter(lambda edge: edge[user_index] == user_id, self.edges))
        else:
            print("User Id not present in the Graph, User Id:", user_id)
            return set()

    def get_user_followers(self, user_id: int, user_index: int= -1):
        if user_id in self.users:
            return set(filter(lambda edge: edge[user_index] == user_id, self.edges))
        else:
            print("User Id not present in the Graph, User Id:", user_id)
            return set()

    def get_user_num_of_friends(self, user_id: int, user_index: int= 0):
        if user_id in self.users:
            return reduce(lambda num_of_friend, edge: num_of_friend + 1 if edge[user_index] == user_id else
                          num_of_friend, self.edges, 0)
        else:
            print("User Id not present in the Graph, User Id:", user_id)

    def get_user_num_of_followers(self, user_id: int, user_index: int= -1):
        if user_id in self.users:
            return reduce(lambda num_of_followers, edge: num_of_followers + 1 if edge[user_index] == user_id else
                          num_of_followers, self.edges, 0)
        else:
            print("User Id not present in the Graph, User Id:", user_id)

    def reset_graph(self):
        self.users.clear()
        self.edges.clear()

    def reset_user_friends(self, user_id: int):
        if user_id in self.users:
            self.edges = set(map(lambda edge: edge[0] != user_id, self.edges))
        else:
            print("User Id not present in the Graph, User Id:", user_id)

    def delete_user_from_graph(self, user_id: int):
        if user_id in self.users:
            self.users.remove(user_id)
            self.reset_user_friends(user_id)
        else:
            print("User Id not present in the Graph, User Id:", user_id)

    def update_input_file(self, input_file_name: str):
        self.input_file = input_file_name

    def construct_graph(self):
        self.reset_graph()
        print("Constructing Graph from file:", self.input_file)
        with open(self.input_file, "r") as graph_file:
            for str_edge in graph_file:
                data_ls = list(map(int, str_edge.split(',')))
                self.add_list_data(data_ls)
        print("Graph Constructed. Number of Users:", self.get_num_of_users(), "Number of Edges:",
              self.get_num_of_edges())


class GraphNodesNeighbors:
    """
    GraphNodesNeighbors -->
        Is responsible  to hold the contents of the graph in the manner as follows:
        { V1:{N11, ... } .... Vn:{Nn1, ... } } (type: dict) --> A dictionary of User Ids as keys mapped to a set of
                                                               the User Ids that are the friends of the user
                                                               corresponding to the user id represented by the key
        Vk (type: int) --> represents a vertex or node (Correspond to a User Id)
        {Nki} (type: set) --> represents the set of friends of the user Vk. Neighbors means that Vk --> Vi. (User Vk
                              follows User Vi)
    """
    def __init__(self, input_file_path: str):
        self.input_file = input_file_path
        self.user_friend_dict = dict()

    def get_users(self):
        return set(self.user_friend_dict.keys())

    def get_friends_of_user(self, user_id: int):
        if user_id in self.user_friend_dict:
            return self.user_friend_dict[user_id]
        else:
            print("User Id not present in the Graph, User ID:", user_id)

    def get_graph(self):
        return self.user_friend_dict

    def add_user(self, user_id: int):
        if user_id not in self.user_friend_dict:
            self.user_friend_dict[user_id] = set()

    def add_user_friend(self, user_id: int, friend_id: int):
        if user_id in self.user_friend_dict:
            if friend_id not in self.user_friend_dict[user_id]:
                self.user_friend_dict[user_id].add(friend_id)
        else:
            print("User Id not present in the Graph, User Id:", user_id)

    def add_list_data(self, ls_data: list):
        if len(ls_data) == 2:
            self.add_user(ls_data[0])
            self.add_user(ls_data[-1])
            self.add_user_friend(ls_data[0], ls_data[-1])
        else:
            print("Input data invalid. Length of the list should be 2. List:", ls_data)

    def get_num_of_users(self):
        return len(self.user_friend_dict)

    def get_num_of_edges(self):
        return reduce(lambda total_num_of_edgs, set_of_friends: total_num_of_edgs + len(set_of_friends),
                      self.user_friend_dict.values(), 0)

    def get_input_file_name(self):
        return self.input_file

    def get_user_friends(self, user_id: int):
        if user_id in self.user_friend_dict:
            return self.user_friend_dict[user_id]
        else:
            print("User Id not present in the Graph, User Id:", user_id)
            return set()

    def get_user_followers(self, user_id: int):
        if user_id in self.user_friend_dict:
            return set(filter(lambda friend_id: user_id in self.user_friend_dict[friend_id],
                              self.user_friend_dict.keys()))
        else:
            print("User Id not present in the Graph, User Id:", user_id)
            return set()

    def get_user_num_of_friends(self, user_id: int):
        if user_id in self.user_friend_dict:
            return len(self.user_friend_dict[user_id])
        else:
            print("User Id not present in the Graph, User Id:", user_id)

    def get_user_num_of_followers(self, user_id: int):
        if user_id in self.user_friend_dict:
            return reduce(lambda num_of_followers, friend_id: num_of_followers + 1 if user_id in
                                                                                      self.user_friend_dict[friend_id] else
                          num_of_followers, self.user_friend_dict.keys(), 0)
        else:
            print("User Id not present in the Graph, User Id:", user_id)

    def reset_graph(self):
        self.user_friend_dict.clear()

    def reset_user_friends(self, user_id: int):
        if user_id in self.user_friend_dict:
            self.user_friend_dict[user_id].clear()
        else:
            print("User Id not present in the Graph, User Id:", user_id)

    def delete_user_from_graph(self, user_id: int):
        if user_id in self.user_friend_dict:
            self.user_friend_dict.pop(user_id)
        else:
            print("User Id not present in the Graph, User Id:", user_id)

    def update_input_file(self, input_file_name):
        self.input_file = input_file_name

    def construct_graph(self):
        self.reset_graph()
        print("Constructing Graph from file:", self.input_file)
        with open(self.input_file, "r") as graph_file:
            for str_edge in graph_file:
                data_ls = list(map(int, str_edge.split(',')))
                self.add_list_data(data_ls)
        print("Graph Constructed. Number of Users:", self.get_num_of_users(), "Number of Edges:",
              self.get_num_of_edges())


if __name__ == '__main__':
    #GraphNodesNeighbors("../../User_Collection/data/user_graph_files/Rumor11/follower_friend_graph.csv
    # ").construct_graph()
    GraphNodesEdges("../../User_Collection/data/user_graph_files/Rumor11/follower_friend_graph.csv").construct_graph()

    print("Hello World!")
