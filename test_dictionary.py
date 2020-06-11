"""Unit Testing for Task 1 and 2"""

__Student_and_Author__ = "Derek Chukwudi Anyanwu"
__docformat__ = 'reStructuredText'
__modified__ = '20/05/2020'
__since__ = '22/05/2020'



import unittest
from hash_table import LinearProbeHashTable
from dictionary import Statistics, Dictionary


def file_len(filename: str) -> int:
    """Calculates the number of lines in a given file"""
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


class TestDictionary(unittest.TestCase):
    DEFAULT_TABLE_SIZE = 250727
    DEFAULT_HASH_BASE = 31
    DEFAULT_TIMEOUT = 10
    FILENAMES = ['english_small.txt', 'english_large.txt', 'french.txt']
    RANDOM_STR = 'FIT1008 is the best subject!'
    
    def setUp(self) -> None:
        """ Used by our test cases """
        self.dictionary = Dictionary(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE)
    
    def test_init(self) -> None:
        """ Testing type of our table and the length is 0 """
        self.assertEqual(type(self.dictionary.hash_table), LinearProbeHashTable)
        self.assertEqual(len(self.dictionary.hash_table), 0)
    
    def test_load_dictionary_statistics(self) -> None:
        """ For each file, doing some basic testing on the statistics generated """
        print("Testing load dictionary statistics method......")
        statistics = Statistics()
        for filename in TestDictionary.FILENAMES:
            words, time, collision_count, probe_total, probe_max, rehash_count = statistics.load_statistics(
                TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE * 2, filename,
                TestDictionary.DEFAULT_TIMEOUT)
            self.assertGreater(words, 0)
            self.assertLess(time, TestDictionary.DEFAULT_TIMEOUT)
            
            # TODO: Add your own test cases here

            # test case 1: # checking list of integers return by load statistics are all integers
            integers = [words, collision_count, probe_total, probe_max, rehash_count]
            assert (all(isinstance(item, int) for item in integers))
    
    def test_load_dictionary(self) -> None:
        """ Reading a dictionary and ensuring the number of lines matches the number of words
            Also testing the various exceptions are raised correctly """
        for filename in TestDictionary.FILENAMES:
            self.dictionary = Dictionary(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE)
            words = self.dictionary.load_dictionary(filename)
            lines = file_len(filename)
            self.assertEqual(words, lines, "Number of words should match number of lines")
        
        # TODO: Add your own test cases (consider testing exceptions being raised)
        # test case 1: # checking it doesnt throw an erro for FileNotFoundError
        print("Testing load dictionary method......work on it")
        filename_2 = 'engli.txt'
        bucket = Dictionary(TestDictionary.DEFAULT_HASH_BASE, TestDictionary.DEFAULT_TABLE_SIZE)
        words = bucket.load_dictionary(filename_2)
        self.assertEqual(words, 0, "Number of words should be 0")
    
    def test_add_word(self) -> None:
        """ Testing the ability to add words """
        # TODO: Add your own test cases
        print("Testing add word......")
        
        # test case 1: inserting hello into the hash table
        self.dictionary.add_word("Hello")
        current_size = len(self.dictionary.hash_table)
        self.assertEqual(current_size, 1, "add word method not working properly")
        
        # test case 2: Insert multiple of item and updating the hash table count
        test_list_2 = ['to', 'customize', 'exception', 'parameters', 'while', 'giving', 'you', 'complete', 'control',
                       'of', 'the active']
        test_list_2_size = len(test_list_2)
        for item in test_list_2:
            self.dictionary.add_word(item)
        current_size = len(self.dictionary.hash_table)
        self.assertEqual(current_size, test_list_2_size + 1, "add word method not working properly")
        
    def test_find_word(self) -> None:
        """ Ensuring both valid and invalid words """
        # TODO: Add your own test cases
        print("Testing find word......")

        # test case 1: converted all the words in the hash table to upper case and check if find word would be able
        # to convert it back to lower case and return true
        self.test_add_word()
        test_list_2 = ['TO', 'CUSTOMIZE', 'EXCEPTION', 'PARAMETERS', 'WHILE', 'GIVING', 'YOU', 'COMPLETE', 'CONTROL',
                       'OF', 'THE ACTIVE']
        for item in test_list_2:
            result = self.dictionary.find_word(item)
            self.assertEqual(result, True, "add word method not working properly")

        # test case 2: finding word not in the dictionary and check if method returns False
        word = "AMAKOHIA"
        result = self.dictionary.find_word(word)
        self.assertEqual(result, False, "find word method not working properly")
        
    def test_delete_word(self) -> None:
        """ Deleting valid words and ensuring we can't delete invalid words """
        print("Testing delete word......")
        self.dictionary.load_dictionary('english_small.txt')
        table_size = len(self.dictionary.hash_table)
        with self.assertRaises(KeyError):
            self.dictionary.delete_word(TestDictionary.RANDOM_STR)
        self.assertEqual(len(self.dictionary.hash_table), table_size)
        
        self.dictionary.delete_word('test')
        self.assertEqual(len(self.dictionary.hash_table), table_size - 1)

    
if __name__ == '__main__':
    unittest.main()
