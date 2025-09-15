import unittest
import re
from functions.get_files_info import get_files_info

class TestFunctions(unittest.TestCase):

    def test_get_main_files(self):
        result = get_files_info("calculator", ".")
        pattern = r"- .*: file_size=\d+ bytes, is_dir=(?:True|False)"
        
        print(result)
        lines = result.strip().split('\n')
        for line in lines:
            self.assertRegex(line, pattern)

    def test_get_pkg_files(self):
        result = get_files_info("calculator", "pkg")
        pattern = r"- .*: file_size=\d+ bytes, is_dir=(?:True|False)"
        
        print(result)
        lines = result.strip().split('\n')
        for line in lines:
            self.assertRegex(line, pattern)

    def test_throw_error(self):
        result = get_files_info("calculator", "/bin")
        
        print(result)
        self.assertEqual(result, 'Error: Cannot list "/bin" as it is outside the permitted working directory')


if __name__ == "__main__":
    unittest.main()
