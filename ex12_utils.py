#################################################################
# FILE : ex12_utils.py
# WRITERS : [noam peled , noampe12 , 207734781], [nicole gurevich,
# nicolegurevich, 322566084]
# EXERCISE : intro2cs2 ex12 2022
# DESCRIPTION : Boggle game, logic part
#################################################################
from boggle_board_randomizer import *


def get_board():
    """func that returns a randomly generated board"""
    board = randomize_board()
    return board


def read_wordlist(filename):
    """func that returns a list of strings
     of the words in the dict"""
    f = open(filename)
    word_lst = f.read()
    return word_lst.split()


def in_range(x, y):
    """check if a given index is inside the board"""
    if 0 <= x < 4 and 0 <= y < 4:
        return True
    else:
        return False


def is_near(x, y):
    """returns all the possible movements of a given placement"""
    lst_possible_near_tuples = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                                (x, y + 1), (x + 1, y + 1), (x + 1, y),
                                (x, y - 1), (x + 1, y - 1)]
    lst_near_tuples = []
    for tup in lst_possible_near_tuples:
        if in_range(tup[0], tup[1]):  # if the index is in range
            lst_near_tuples.append(tup)  # add it to the final list
    return lst_near_tuples


def is_valid_path(board, path, words):
    """check if the path follows a valid direction
        and if the word created is in the words list"""
    user_word = []
    for letter in path:  # letter is an index (ex: (0,1))
        y = letter[0]
        x = letter[1]
        if not in_range(x, y):
            return None
        user_word.append(board[y][x])  # if the index of the letter is in
        # range add it to the user word
    user_word = "".join(user_word)
    if user_word not in words:  # if the word that the path built is not
        # in the words_lst
        return None
    used_path = []
    for i in range(len(path)-1):
        used_path.append(path[i])  # save index's that were already used
        if path[i+1] not in is_near(path[i][0], path[i][1]) or path[i+1] \
                in used_path:  # if a step was already used or
            # if the step after it is not a possible move
            return None
    return user_word


def indices_of_board(board):
    """returns a list of all the indices on the board"""
    indices = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            indices.append([(i, j)])
    return indices


def find_length_n_paths(n, board, words):
    """main func for find_length_n_paths
        finds all the possible words you can
        find on the board with a certain path length"""
    possible_paths = []
    indices = indices_of_board(board)
    if n > len(board) * len(board[0]):  # if path is longer then the cubes
        # on the board
        return []  # the path doesn't exist
    for indx in indices:
        cur_word = board[indx[0][0]][indx[0][1]]  # a single letter that
        # will become the current word we are searching for
        find_length_n_paths_helper(n, cur_word, words, board, indx,
                                   possible_paths)  # call the helper function
    return possible_paths


def find_length_n_paths_helper(n, cur_word, words, board, path, possible_paths):
    """helper function for find_length_n_paths
    the starting path is the index given by the main func"""
    filtered_words = []
    for word in words:
        if str(cur_word) in word:  # if the letter\part of the current word
            # is in the word add it to the filtered words list for later use
            filtered_words.append(word)
    if len(filtered_words) == 0:  # if none of the words fit the current word
        # return an empty list
        return []
    if len(path) == n and cur_word in filtered_words:  # if the length of the
        # path equals to n and the current word is in the filtered list
        return possible_paths.append(path[:])
    for idx in is_near(path[-1][0], path[-1][1]):  # check near indices
        if len(path) <= n - 1:
            if idx not in path:
                find_length_n_words_helper(filtered_words,
                                           cur_word + board[idx[0]][idx[1]],
                                           board, path + [idx], possible_paths)
                # call recursively with longer word and path
    return possible_paths


def find_length_n_words(n, board, words):
    """main func for find_length_n_words
        finds all the possible words with a certain length
         on the board """
    possible_paths = []
    indices = indices_of_board(board)
    lst_of_words = words_filter(words, n)
    for indx in indices:
        cur_word = board[indx[0][0]][indx[0][1]]  # a single letter that
        # will become the current word we are searching for
        find_length_n_words_helper(lst_of_words, cur_word,
                                   board, indx, possible_paths) # call the
        # helper function
    return possible_paths


def find_length_n_words_helper(lst_of_words, cur_word, board, path,
                               possible_paths):
    """helper function for find_length_n_words
        works almost exactly the same as find_length_n_paths_helper"""
    filtered_words = []
    for word in lst_of_words:
        if str(cur_word) in word:
            filtered_words.append(word)
    if len(filtered_words) == 0:
        return []
    if cur_word in filtered_words:
        return possible_paths.append(path[:])
    for idx in is_near(path[-1][0], path[-1][1]):
        if len(path) <= 15:  # if the length of the
            # word is longer than the board
            if idx not in path:
                find_length_n_words_helper(filtered_words,
                                           cur_word + board[idx[0]][idx[1]],
                                           board, path+[idx], possible_paths)
    return possible_paths


def words_filter(words, n):
    """helper func- words filter for find_length_n_words"""
    new_words = []
    for word in words:
        if n == len(word):
            new_words.append(word)
    return new_words


def max_score_paths(board, words):
    """return for each word the path that gives the maximum score """
    path_list = []
    for word in words:
        n = len(word)
        paths = find_length_n_words(n, board, [word])
        if paths:  # if path exists
            path_list.append(max(paths, key=lambda x: len(x)))
    return path_list
