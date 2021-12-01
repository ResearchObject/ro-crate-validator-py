import sys
sys.path.insert(0, '..')
import os
import os.path
import unittest
from unittest.mock import patch
from src.basic_check import file_size_check
from src.basic_check import existence_check

class TestBasicCheckFunction(unittest.TestCase):

    @patch('builtins.input', return_value = 'gzfile.gz')
    def test_existence_function(self, mock_input):
    	os.chdir(os.path.dirname(os.path.join(os.getcwd(), 'samples/test-data/')))
    	result = existence_check(mock_input())
    	self.assertEqual(result, 'gzfile', 'Check Existence Function Test -- FAIL')

    @patch('builtins.input', return_value = 'zipfile.zip')
    def test_size_check(self, mock_input):
    	result = file_size_check(mock_input())
    	self.assertTrue(result, 'File Size Check Test -- FAIL')


if __name__ == '__main__':
    unittest.main()

