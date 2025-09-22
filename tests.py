import unittest
import re
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

class TestFunctions(unittest.TestCase):

    def test_get_main_files(self):
        result = get_files_info("calculator", ".")
        pattern = r"- .*: file_size=\d+ bytes, is_dir=(?:True|False)"
        
        # print(result)
        lines = result.strip().split('\n')
        for line in lines:
            self.assertRegex(line, pattern)

    def test_get_pkg_files(self):
        result = get_files_info("calculator", "pkg")
        pattern = r"- .*: file_size=\d+ bytes, is_dir=(?:True|False)"
        
        # print(result)
        lines = result.strip().split('\n')
        for line in lines:
            self.assertRegex(line, pattern)

    def test_throw_error(self):
        result = get_files_info("calculator", "/bin")
        
        # print(result)
        self.assertEqual(result, 'Error: Cannot list "/bin" as it is outside the permitted working directory')

    def test_get_file_content(self):
        result = get_file_content("calculator", "lorem.txt")

        # self.assertLessEqual(len(result), 10_000)

        result_main = get_file_content("calculator", "main.py")

        # print(result_main)

        # self.assertLessEqual(len(result_main), 10_000)

        result_pkg = get_file_content("calculator", "pkg/calculator.py")

        # print(result_pkg)
        # self.assertLessEqual(len(result_pkg), 10_000)

        result_err = get_file_content("calculator", "/bin/cat")
        
        # print(result_err)

        # self.assertEqual(result_err, 'Error: Cannot read "/bin/cat" as it is outside the permitted working directory')

        result_err_exist = get_file_content("calculator", "pkg/does_not_exist.py")

        # self.assertEqual(result_err_exist, 'Error: File not found or is not a regular file: "pkg/does_not_exist.py"')

    def test_write_to_file(self):
        result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
        # print(result)

        result_1 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        # print(result_1)

        result_2 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        # print(result_2)

    def test_run_python_file(self):
        result = run_python_file("calculator", "main.py")
        print(result)

        result = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result)

        result = run_python_file("calculator", "tests.py")
        print(result)

        result = run_python_file("calculator", "../main.py")
        print(result)

        result = run_python_file("calculator", "nonexistent.py")
        print(result)
    
        

if __name__ == "__main__":
    unittest.main()
