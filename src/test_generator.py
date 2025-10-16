import unittest

from generator import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_basic_header(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_header_with_spaces(self):
        markdown = "#   My Page Title   "
        self.assertEqual(extract_title(markdown), "My Page Title")

    def test_header_among_other_text(self):
        markdown = "# Welcome\n\nThis is my markdown file."
        self.assertEqual(extract_title(markdown), "Welcome")

    def test_no_header_raises_exception(self):
        markdown = "This markdown has no h1 title"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_multiple_headers(self):
        markdown = "# First\n\n## Second\n\n### Third"
        self.assertEqual(extract_title(markdown), "First")

if __name__ == '__main__':
    unittest.main()