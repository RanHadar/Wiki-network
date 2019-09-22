#############################################################
# FILE : article.py
# WRITER : Ran_Hadar , ranhadar , 305493389
# EXERCISE : intro2cs ex10 2016-2017
# DESCRIPTION: A simple program runs a wikinetwork
############################################################
# Imports
import copy
############################################################

INITIAL_RANK = 1
INITIAL_DEGREE = 0


class Article:
    def __init__(self, article_title):
        self.__article_title = article_title
        self.__neighbors = list()  # list of the article's neighbors
        self.__money = INITIAL_RANK
        self.__degree = INITIAL_DEGREE

    def get_title(self):
        """"
        Returns article's title
        """
        return self.__article_title

    def add_neighbor(self, neighbor):
        """"
        Gets a neighbor and updated the list of neighbors
        if its not inside
        """
        if neighbor not in self.__neighbors:
            self.__neighbors.append(neighbor)

    def get_neighbors(self):
        """
        Returns a list of neighbors
        """
        return self.__neighbors

    def get_degree(self):
        """"
        Returns the degree of the article
        """
        return self.__degree

    def set_degree(self):
        """
        Sets the degree of the article
        """
        self.__degree += 1

    def __repr__(self):
        """"
        Returns a string represents the article by parameters
        """
        list_neighbors_names = list()
        for neighbor in self.__neighbors:
            list_neighbors_names.append(neighbor.get_title())
        tuple_info = (self.__article_title, list_neighbors_names)
        return str(tuple_info)

    def __len__(self):
        """"
        Returns a number of the article's neighbors
        """
        len_neighbors = len(self.__neighbors)
        return len_neighbors

    def __contains__(self, article):
        """"
        Returns True or False if an article is in the collection
        """
        if article in self.__neighbors:
            return True
        else:
            return False

    def get_degree(self):
        """
        :return: the degree of the article
        """
        return self.__degree

    def set_degree(self):
        """"
        Sets the degree of an article plus 1
        """
        self.__degree += 1






