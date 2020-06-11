""" This module implements the dictionary by a Hash Table using Linear Probing for conflict resolution.
Module consist of the following class and methods:
Class: Dictionary, Statistics
Method: load_dictionary, add_word, find_word, delete_word, menu
"""

__author__ = "Derek Chukwudi Anyanwu"


from typing import Tuple
from hash_table import LinearProbeHashTable
import timeit
import string
import csv
import os


class InvalidInputError(Exception):
    """ Exception  to be thrown when the input given was not expected."""
    pass


class Dictionary:
    """Creates a new Hash Table with the given hash base and initial table size"""
    VALUE = 1  # associated data of the item in the hash table
    
    def __init__(self, hash_base: int, table_size: int) -> None:
        """ Construction function that initialize an instance of class LinearProbeTable with variable self.hash_table"""
        self.count = 0  # how many items have been stored
        self.hash_base = hash_base
        self.table_size = table_size
        
        # created a Dictionary instance of LinearProbeHashTable
        self.hash_table = LinearProbeHashTable(self.hash_base, self.table_size)
        self.duration = 0  # Total time taken to add item from file to dictionary
    
    def load_dictionary(self, filename: str, time_limit: int = None) -> int:
        """ Reads a file filename containing one word per line (ignoring the new line character), and adds each word
        to self.hash_table with integer 1 as the associated data

        The time complexity of strip function is  O(n) and The time complexity of readLines function is  O(m) so
        @complexity: Best O(n*m) and worst O(n*m)
        """
        startTime = timeit.default_timer()  # starting time counter
        deltaTime = 0
        try:
            # with the with-statement, no need to call file.close()
            with open(filename, 'r', encoding="UTF-8") as handle:  # Open file on read mode
                # method readlines()reads the entire line from the file and pass it to line
                # line.strip() removes the Leading and trailing whitespaces and pass it to key
                for line in handle.readlines():
                    key = line.strip()
                    deltaTime = timeit.default_timer() - startTime  # time difference
                    if time_limit is not None and deltaTime >= time_limit:
                        deltaTime = time_limit  #
                        raise TimeoutError
                    self.hash_table[key] = self.VALUE  # assigning 1 to the key and storing it in the dictionary
                    self.count += 1  # increment the number of words in the dictionary
        except TimeoutError:  # catches error when time run out reading a file into a dictionary
            raise TimeoutError
        except IOError:
            # print('File is not accessible')
            pass
        finally:  # This will always run
            self.duration = deltaTime  # Total time it took to read the file
            return self.count  # always runs
    
    def add_word(self, word: str) -> None:
        """ Method adds the given word to the Hash Table with integer 1 as their associated data.

        :pre-condition: word is a single word.
        :post-condition: The given word is in its lowercase.
        @complexity: Best O(1) and worst O(n) where n is the number of chars to convert to lower case
        """
        if word not in string.ascii_lowercase:
            word = word.lower()  # convert all the char to its lowercase
        self.hash_table[word] = self.VALUE
    
    def utility(self, filename, max_time: int = None):
        """ Utility method of hash table returns the hash table, total time adding item to hash table
        the len of hashtable.
        @complexity: Best O(n*m) and worst O(n*m)
        """
        self.load_dictionary(filename, max_time)
        return self.hash_table, self.duration, self.count
    
    def find_word(self, word: str) -> bool:
        """Determines whether the item is in the hash table
         :complexity: O(1) in best case, O(N) in worst case as n the number of char to convert to lower
         """
        if word not in string.ascii_lowercase:
            word = word.lower()
        try:
            _ = self.hash_table[word]
        except KeyError:
            return False
        else:
            return True
    
    def delete_word(self, word: str) -> None:
        """Deletes given word from the Hash Table
        
        :post-condition: File is deleted from the Hash Table.
        :complexity: O(1) in best case, O(N) in worst case
        """
        try:
            self.find_word(word)
        except KeyError:
            pass
        else:
            if word not in string.ascii_lowercase:
                word = word.lower()
            # del self.hash_table[word]
            
            self.hash_table.__delitem__(word)
    
    def command_read_file(self, filename: str) -> None:
        """Read a file into a dictionary.

        :precondition: the file exit.
        :post-condition: File read into the dictionary.
        @complexity: Best O(n*m) and worst O(n*m), n is the no of words in the file, m is the no of char in the word
        Raises an exception if the input word is not valid
        """
        try:
            # checking if file is readable and closeable
            handle = open(filename, 'r')  #
            handle.close()
        except IOError:
            print('File is not accessible')
            print("Please enter a valid file!")
        else:
            self.load_dictionary(filename, time_limit=None)
            print("Successfully read file")
    
    def command_enter_word(self, word: str) -> None:
        """Enter word into the hash table.

        :pre-condition: the string word is a single word.
        :post-condition: New word inserted into the hash table.
        @complexity: Best O(1) and worst O(n)
        # Raises an exception if the input word is not valid
        """
        try:
            words = word.split()
            # checking if its really a word or more than a word
            # checking if its a string
            if len(words) > 1 or not isinstance(word, str):
                raise ValueError
        except ValueError:
            print("Please enter valid word!")
        else:
            self.add_word(word)
            print(word, "successfully added")
    
    def command_found_word(self, word: str) -> None:
        """Method Search for the given word in the hash table
        :complexity: O(1) in best case, O(N) in worst case, n due to lower() used in find_word method
        """
        try:
            words = word.split()
            if len(words) > 1 or not isinstance(word, str):
                raise ValueError
        except ValueError:
            print("Please enter a valid word!")
        else:
            if self.find_word(word):
                print(word, "found in dictionary")
            else:
                print(word, "not in the dictionary")
    
    def command_delete_word(self, word: str) -> None:
        """Delete a word from the hash table.

        :pre-condition: The dictionary is not empty.
        :post-condition: The word is deleted.
        :complexity: O(1) in best case, O(N) in worst case
        # Raises an exception if the input word is not valid
        """
        try:
            words = word.split()  # method split word if has strings with spaces in between
            if len(words) > 1 or not isinstance(word, str):
                raise ValueError
            if not self.find_word(word):
                raise InvalidInputError
        except ValueError:
            print("Please enter a valid word!")
        except InvalidInputError:
            print(word, "not found in the dictionary!")
        else:
            self.delete_word(word)
            print(word, "Deleted from dictionary")
    
    def command_exit(self) -> None:
        """ Quit the program.
        :pre-condition: Program is still running.
        :post-condition: Program end.
        :complexity: O(1) in best case, O(1) in worst case
        """
        exit()
    
    def menu(self) -> None:
        """ Print the menu of commands
        :complexity: O(1) in best case, O(n*m) in worst case
        """
        line1 = "1. Read File"
        line2 = "2. Add Word"
        line3 = "3. Find Word"
        line4 = "4. Delete Word"
        line5 = "5. Exit"
        print(line1, line2, line3, line4, line5, sep='\n')
        user_input = input("Enter option: ")
        
        # -------------------------------------------------------------------------
        # Reading a file from the command prompt
        if user_input == '1':
            input_file = input("Enter filename: ")
            self.command_read_file(input_file)  # method to read file into the hash table
        
        # -------------------------------------------------------------------------
        # Adding word to the hash table
        elif user_input == '2':
            input_word = input("Enter word: ")
            self.command_enter_word(input_word)
        
        # -------------------------------------------------------------------------
        # Finding word in the hash table
        elif user_input == '3':
            found_word = input("Enter word: ")
            self.command_found_word(found_word)  # method to find the word in the hash table
        
        # -------------------------------------------------------------------------
        # Deleting word in the hash table
        elif user_input == '4':
            delete_word = input("Enter word: ")
            self.command_delete_word(delete_word)
        
        # -------------------------------------------------------------------------
        # Exit the menu
        elif user_input == '5':
            self.command_exit()
        
        self.menu()  # call menu back until user enter 5, exit


class Statistics:
    """ Class collect, organize, analyze, interprete and present words, time, collision_count,
    probe_total, probe_max, rehash_count.
    """
    
    def load_statistics(self, hash_base: int, table_size: int, filename: str, max_time: int) -> Tuple:
        """ Method creates a new dictionary with hash_base and table_size
        :@complexity: Best O(n*m) and worst O(n*m) from reading the file in the hash table
        """
        container = Dictionary(hash_base, table_size)  # creating object of the Dictionary
        hash_table, deltaTime, table_length = container.utility(filename, max_time)
        collision_count, probe_total, probe_max, rehash_count = hash_table.statistics()
        return table_length, deltaTime, collision_count, probe_total, probe_max, rehash_count
    
    def table_load_statistics(self, max_time: int) -> None:
        """ method for each of these dictionaries and each combination of the values specified in the table below for TABLESIZE
        and b in the universal hash function, uses load_statistics to time how long it takes for load_dictionary to run
        and prints a line to file output task2.csv
        @complexity: Best O(1) and worst O(n) as n complexity of summing the prochainlength
        """
        files = ['english_small.txt', 'english_large.txt', 'french.txt']
        bases = [1, 27183, 250726]
        table_sizes = [250727, 402221, 1000081]
        combination_list = []
        for file in files:
            for base in bases:
                for table_size in table_sizes:
                    table_length, elapsed_time, collision_count, probe_total, probe_max, rehash_count = self.load_statistics(
                        base, table_size, file, max_time)
                    
                    # append to combinationsList at each iteration
                    combination_list.append((file, table_size, base, table_length, collision_count, probe_total,
                                             probe_max, rehash_count, elapsed_time))
        
        filename = "output_task2.csv"
        if os.path.isfile(filename):  # if the file already exists, remove it.
            os.remove(filename)
            outfile2 = open('./output_task2.csv', 'w')
            writer = csv.writer(outfile2)
            writer.writerow(
                ["File Name", "Table Size", "Hash Base", "Words", "Collisions", "Probes",
                 "Probe Max", "Rehash", "Time"])  # Heading of the csv file
            writer.writerows(combination_list)
            outfile2.close()
        
        else:
            # Saving to csv
            outfile2 = open('./output_task2.csv', 'w')
            writer = csv.writer(outfile2)
            writer.writerow(
                ["File Name", "Table Size", "Hash Base", "Words", "Collisions", "Probes",
                 "Probe Max", "Rehash", "Time"])  # Heading of the csv file
            writer.writerows(combination_list)
            outfile2.close()


#
# if __name__ == '__main__':
#     "The main function to test time consumed for each combination of the values for table size and b"
#
# bucket = Dictionary(250726, 1000081)
# bucket.menu()

# print(bucket.load_dictionary('note12.txt', 0.01))
# bucket.load_dictionary('note12.txt', None)
#
# statistics = Statistics()
# statistics.table_load_statistics(10)
