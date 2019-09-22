#############################################################
# FILE : wikinetwork.py
# WRITER : Ran_Hadar , ranhadar , 305493389
# EXERCISE : intro2cs ex10 2016-2017
# DESCRIPTION: A simple program runs a wikinetwork
############################################################
# Imports
import article as ar
import copy
############################################################
INITIAL_MONEY_GIVEN = 0.9
REMNANT_MONEY = 0.1


def read_article_links(file_name):
    """"
    Gets a text file with articles and links and
    returns a list of tuples
    """
    articles_list = list()
    with open(file_name, 'r') as articles_file:  # read mode
        for line in articles_file:
            # reads every line and turns it to a list of tupples
            list_line = line.split()
            tuple_line = (list_line[0],list_line[1])
            articles_list.append(tuple_line)

    return articles_list

class WikiNetwork:

    def __init__(self, link_list):
        self.__link_list = link_list # the given file
        self.__articles_dict = dict() # a collection of articles
        self.__update_wiki(link_list) # function that updates the collection
        self.__articles_degree = set() # a set with all the articles degrees
        self.__degrees_collection() # function that initialize all articles degrees
        self.__ranks_dic = dict() # dict with all titles and ranks
        self.__temp_ranks_dic = dict() # temp dict to ranks
        self.__update_ranks() # function that initialize all articles ranks




    def __update_wiki(self,link_list):
        """"
         Gets a list of tuples with articles and links and builds
         the network by the given values
        """
        for tuple_art in link_list:
            if tuple_art[0] not in self.__articles_dict:
                self.__articles_dict[tuple_art[0]] = ar.Article(tuple_art[0])
            if tuple_art[1] not in self.__articles_dict:
                self.__articles_dict[tuple_art[1]] = ar.Article(tuple_art[1])
            self.__articles_dict[tuple_art[0]].add_neighbor(self.__articles_dict[tuple_art[1]])

    def update_network(self, link_list):
        """"
         Gets a list of tuples with articles and links and updates
         the network by the given values
        """
        self.__update_wiki(link_list)

    def __update_ranks(self):

        for article in self.get_titles():
            self.__ranks_dic[article] = INITIAL_MONEY_GIVEN
            self.__temp_ranks_dic[article] = INITIAL_MONEY_GIVEN

    def page_rank(self, iters, d = INITIAL_MONEY_GIVEN):
        """"
        Gets a number of iteration and a number and returns a
        sorted list of articles titles in the net by their rank
        """
        list_articles = self.get_articles()
        for i in range(iters):
            for article in list_articles:
                if len(article.get_neighbors()) > 0:  # if the article as neighbors
                    article_title = article.get_title()
                    # calculates the money to pass to neighbors
                    dvided_money = (d * self.__ranks_dic[article_title])\
                                   / (len(article.get_neighbors()))
                    for neighbor in article.get_neighbors():
                        # gives to each neighbor the money
                        self.__temp_ranks_dic[neighbor.get_title()] += dvided_money
                    self.__temp_ranks_dic[article_title] -= \
                        self.__ranks_dic[article_title]
                    # sets the new rank for this iter to the article
                    self.__temp_ranks_dic[article_title] += REMNANT_MONEY
            self.__ranks_dic = copy.deepcopy(self.__temp_ranks_dic)
        # sorting the list
        tuple_ranks_list = self.__ranks_dic.items()
        tuple_ranks_list = sorted(tuple_ranks_list, key=lambda x: (-x[1], x[0]))
        return [tup[0] for tup in tuple_ranks_list]


    def jaccard_index(self,article_title):
        """"
         Gets a title of an article and returns a sorted list of articles
         titles in the net by their jaccard index relates to the given title
        """
        list_distance = list()
        list_articles = self.get_titles()
        if article_title not in list_articles: # if the article doesnt found
            return None
        article1 = self.__articles_dict[article_title]
        article1_neighbors = set(article1.get_neighbors())
        if article1_neighbors:
            for article in list_articles:
                if article != article_title:
                    article2 = self.__articles_dict[article]
                    article2_neighbors = set(article2.get_neighbors())
                    intersection = len(article1_neighbors&article2_neighbors)
                    union = len(article1_neighbors | article2_neighbors)
                    distance = abs(intersection / union) # calculates the distance
                elif article == article_title:
                    distance = 1  # if the article is the one
                elif not article1_neighbors: # if there are no neighbors
                    return None
                # builds a tupple with the relevant info
                list_distance.append((article, distance))
            # sorts the tuple
            list_distance = sorted(list_distance, key=lambda x: (-x[1],x[0]))

            return [tup[0] for tup in list_distance]
        else:
            return None

    def __degrees_collection(self):
        """"
        Sets all the articles degrees in the network
        """
        for tuple_article in self.__link_list:
            title = tuple_article[1]
            self.__articles_dict[title].set_degree()


    def travel_path_iterator(self, article_title):
        """"
        Gets a title of an article and returns his
        linked path in the new using a generator by moving to
         the max linked neighbor
        """
        if article_title not in self.get_titles():
            return
        article_obj = self.__articles_dict[article_title]
        neighbors_set = article_obj.get_neighbors()
        yield article_title  # yield the first article

        while neighbors_set:  # while not empty
            neighbors_degrees = set()
            for neighbor in neighbors_set:
                neighbors_degrees.add(neighbor.get_degree())

            max_degree_neig = max(neighbors_degrees)  # finds the max degree
            max_neighbors_list = list()

            for neighbor in neighbors_set:
            # build a list with the max values to sort
            # them after lexicographically
                 if neighbor.get_degree() == max_degree_neig:
                    max_neighbors_list.append(neighbor.get_title())
            # finds the min lexi from the max list
            min_lexi = min(max_neighbors_list)
            yield min_lexi # yield the min neighbor
            # turns the relavent article obj to be the min found
            article_obj = self.__articles_dict[min_lexi]
            neighbors_set = article_obj.get_neighbors()



    def friends_helper(self, article_title, depth, set_path):
        """"
        Gets a title of an article, path and a set and returns a updated
         set with the relevant neighbors of the articles
        regards the path giving.
        """
        if depth == 0 and self.__articles_dict[article_title].get_neighbors() is not None:
            return
        else:
            for neighbor in self.__articles_dict[article_title].get_neighbors():
                neighbor_title = neighbor.get_title()
                set_path.add(neighbor_title)
                # recursion downgrade the depth by 1 until reaches to the base
                self.friends_helper(neighbor_title, depth - 1, set_path)


    def friends_by_depth(self, article_title, depth):
        """"
        Gets a title of an article and a path returns a updated
         set with the relevant neighbors of the articles
        regards the path giving.
        """
        if article_title not in self.__articles_dict:
            return None
        else:  # goes to the helper and does the recursion
            set_path = set()
            set_path.add(article_title)
            self.friends_helper(article_title, depth, set_path)
            return set_path  # returns the relevant path by depth


    def get_articles(self):
        """"
        Returns a list of objects of articles
        """
        list_articles_obj = list()
        for article in self.__articles_dict.values():
            list_articles_obj.append(article)
        return list_articles_obj

    def get_titles(self):
        """
        Returns a list of articles titles
        """
        list_articles_str = list()
        for article in self.__articles_dict.keys():
            list_articles_str.append(article)
        return list_articles_str

    def __contains__(self, item):
        """
        Gets an item and returns True if its in the network, else False
        """
        if item in self.__articles_dict:
            return True
        else: return False

    def __len__(self):
        """"
        Returns the number of articles in the net
        """
        return len(self.__articles_dict)

    def __repr__(self):
        """"
        Prints the network
        """
        return str(self.__articles_dict)

    def __getitem__(self, item):
        """
        Checks if a title is in the network
        returns its object
        """
        if item in self.__articles_dict:
            return self.__articles_dict[item]






