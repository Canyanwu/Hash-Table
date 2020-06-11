""" This module implements the Hash Table to read and maintain a dictionary of words.
Module consist of the following class, methods and function:
Classes: Frequency, Rarity
Methods: load_dictionary, normalize_word, add_file, rarity, ranking, custom_sort
Function: frequency_analysis,
"""

__author__ = "Derek Chukwudi Anyanwu"


from enum import Enum
from typing import Tuple
from dictionary import Dictionary
from hash_table import LinearProbeHashTable
from list import ArrayList
import sys
import string

sys.setrecursionlimit(50000)  # recursion limit increase


def frequency_analysis() -> None:
    """Function create an object of the Frequecny class and add file to the hash table using the add_file method of
     the Frequency class, reads from the cmd prompt the number of ranking the user wants to display, calls the ranking
     method and print the ranking, the word, frequency and the rarity of the word.
     :complexity: O(1) in best case, O(1) in worst case
    """
    
    frequent = Frequency()
    frequent.add_file('215-0.txt')
    try:
        user_input = int(input("Enter number of ranking to display: "))
    except ValueError:
        print("Please enter a  valid number!")
    else:
        array_output = frequent.ranking()
        for item in range(user_input):
            print("Ranking: " + str(item) + "   " + "Word: " + str(array_output[item][0]) + "   " + "Frequency: "
                  + str(array_output[item][1]) + "   " + "Rarity: " + str(frequent.rarity(array_output[item][0])))


class Rarity(Enum):
    """ Class initialize enum members that composed of name and a value."""
    COMMON = 1
    RARE = 2
    UNCOMMON = 3
    MISSPELT = 4


class Frequency:
    """ Class uses Linear Probing hash table to create dictionary and perform frequency analysis on a set of files."""
    HASH_BASE = 250726  # constant
    TABLE_SIZE = 1000081  # constant
    
    def __init__(self) -> None:
        self.hash_table = LinearProbeHashTable(self.HASH_BASE, self.TABLE_SIZE)  # storage for new words to be read in
        self.dictionary = Dictionary(self.HASH_BASE, self.TABLE_SIZE)  # instance of the DIctionary object
        self.dictionary.load_dictionary("english_large.txt", time_limit=None)  # read in filenameto the dictionary
        self.warehouse = self.dictionary.hash_table  # storage for the dictionary of words
        self.max_word = (None, 0)  # tuple containing max word and its frequency
        self.highest_occurrence = 0  # frequency of most occuring word in the read file
    
    def normalize_word(self, text: str) -> str:
        """Method returns the lower case of a word, remove punctuation at the start and end of a word, whitespace
        and strip away all unwanted characters
        
        :complexity: O(1) in best case, O(N) in worst case as N is the number of chars in the txt
        """
        
        def remove_punctuation(my_text: str) -> str:
            return my_text.strip(string.punctuation)
        
        def new_line_char(my_text: str) -> str:
            return my_text.rstrip()
        
        def lower(my_text: str) -> str:
            return my_text.lower()
        
        return lower(new_line_char(remove_punctuation(text)))
    
    def add_file(self, filename: str) -> None:
        """Method validated a file taht a file is readable and closeable and if its  then calls words_in_dictionary.
        Raises an exception if the input file is not valid
        """
        try:
            # checking if file is readable and closeable
            handle = open(filename, 'r')  #
            handle.close()
        except IOError:
            print("'" + filename + "'", 'File is not accessible')
            pass
        else:
            self.words_in_dictionary(filename)
    
    def words_in_dictionary(self, filename: str) -> None:
        """Method reads words from a valid file into a hash table only if it exit in the dictionary of words called the
        warehouse and updates its occurence in such a way that the data associated to the word is its “occurrence count.
        :complexity: O(N) in best case, O(N)* Complexity of normalize_word method  in worst case as n is the numbe od words
        """
        with open(filename, 'r', encoding="UTF-8") as handle:  # Open file on read mode
            for word in handle.read().split():
                key = self.normalize_word(word)  # removes unwanted characters and punctuations
                try:
                    # NOTE: key here is a word
                    self.warehouse[key]  # checking if word exit in the dictionary
                except KeyError:
                    pass
                else:
                    try:
                        # At this stage the word exit inthe dictionary which is the warehouse,
                        # So now we check if the word exit in hash table already or not.
                        # if this word is already exist in the table, increment the count by 1
                        if self.hash_table[key]:
                            self.hash_table[key] += 1
                    except KeyError:
                        self.hash_table[key] = 1  # first occurrence of this word, frequency set to 1
                        pass
                    else:
                        # keeps track of the highest occurence, and the associated word.
                        if self.hash_table[key] > self.highest_occurrence:
                            self.highest_occurrence += 1
                            self.max_word = (key, self.hash_table[key])
    
    def rarity(self, word: str) -> Rarity:
        """ Method accept a word as arqument and returns its rarity score as an enumerated value
        which explains whether the word is a common, uncommon or rare on a given text file.
        :complexity: O(1) in best case, O(1) in worst case
        """
        try:
            self.hash_table[word]
        except KeyError:
            return Rarity.MISSPELT  # if the word is not in the hash table, probably its most probably typo error
        else:
            if self.hash_table[word] >= self.highest_occurrence / 100:
                return Rarity.COMMON
            elif self.hash_table[word] < self.highest_occurrence / 1000:
                return Rarity.RARE
            else:  # self.highest_occurrence / 1000 <= self.hash_table[word] < self.highest_occurrence / 100:
                return Rarity.UNCOMMON
    
    def ranking(self) -> ArrayList[Tuple]:
        """Method create storage space of ArrayList type of same size of the hash table and transfers not None items of
        the hash table into it and calls the sorting method to sort it based on sorting type.
        :complexity: Nlog(N)*CompEq in best case when the pivot is the median value, O(N2)*CompEq in worst case
        when the pivot is max/ min
        """
        # 1 is sorting by descending order and 2 is sorting by ascending order(Not implemented here though)
        # Only run is hash table is not empty. 
        if not self.hash_table.is_empty():
            order_by = 1  # sorting by descending order
            ranking_array = ArrayList(len(self.hash_table))
            index = 0
            for item in self.hash_table:
                if item is not None:
                    ranking_array.insert(index, item)
                    index += 1
            self.custom_sort(ranking_array, order_by)
            return ranking_array
    
    def custom_sort(self, the_array: ArrayList, order_by: int) -> ArrayList:
        """method sort an ArrayList in descending order using quick sort
        :complexity: Nlog(N)*CompEq in best case when the pivot is the median value, O(N2)*CompEq in worst case
        when the pivot is max/ min
        """
        
        def quick_sort(array: ArrayList) -> ArrayList:
            start = 0
            end = len(array) - 1
            print("........ Sorting Start .......")
            quick_sort_aux(array, start, end)
            print("........ Done sorting ........")
            return array  # its finally sorted
        
        def quick_sort_aux(array: ArrayList, start: int, end: int) -> None:
            if start < end:
                boundary = partition(array, start, end)  # get the boundary
                quick_sort_aux(array, start, boundary - 1)  # pivot becomes
                quick_sort_aux(array, boundary + 1, end)
        
        def partition(array: ArrayList, start: int, end: int) -> int:
            """ """
            mid = (start + end) // 2
            pivot = array[mid][1]  # Select the pivot element
            array[start], array[mid] = array[mid], array[start]
            boundary = start
            for k in range(start + 1, end + 1):
                if order_by == 1:  # sorting descending
                    # swap all elements greater than the pivot with the array at the next boundary of the array
                    if array[k][1] > pivot:
                        boundary += 1
                        array[k], array[boundary] = array[boundary], array[k]  # swapping
                
                if order_by == 2:  # sorting ascending
                    if array[k][1] < pivot:
                        boundary += 1
                        array[k], array[boundary] = array[boundary], array[k]  # swapping
            
            # Put the pivot back in its final place
            array[start], array[boundary] = array[boundary], array[start]  # swapping
            return boundary
        
        return quick_sort(the_array)


# if __name__ == '__main__':
#     "The main function to test time consumed for each combination of the values for table size and b"
#
# frequency_analysis()

# fre = Frequency()
# fre.add_file('215-0.txt')
# print(fre.ranking())

# fre.add_file('2600-0.txt')
# fre.add_file('1342-0.txt')
# fre.add_file('215-0.txt')
# print(fre.add_file('98-0.txt'))
# # print(fre.add_file('hello_word.txt'))
# # print(fre.add_file('note12.txt'))
# print(fre.groub_by_frequency())
# print(fre.rarity("hhifff"))
