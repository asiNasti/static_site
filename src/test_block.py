import unittest
from block import BlockType
from block import block_to_block_type, markdown_to_blocks

class TestBlocks(unittest.TestCase):
    def test_full_split(self):
        markdown_text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        actual_nodes = markdown_to_blocks(markdown_text)
        expected_nodes = ["This is **bolded** paragraph",
                          "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                          "- This is a list\n- with items"]
        
        self.assertListEqual(actual_nodes, expected_nodes)
    
    def test_no_splitting_on_single_newline(self):
        markdown_text = "Just one block.\nThis line is still part of it.\nAnd so is this."
        expected_blocks = ["Just one block.\nThis line is still part of it.\nAnd so is this."]

        self.assertListEqual(markdown_to_blocks(markdown_text), expected_blocks)

    def test_empty_input(self):
        self.assertListEqual(markdown_to_blocks(""), [])
        self.assertListEqual(markdown_to_blocks("\n\n\t  \n"), [])


class TestBlocks(unittest.TestCase):
    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEAD)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEAD)

        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH) 
    
    def test_quote_block(self):
        quote_text = "> This is line one\n> This is line two\n> Final line."
        self.assertEqual(block_to_block_type(quote_text), BlockType.QUOTE)
        
        invalid_quote = "> First line\nSecond line is missing prefix"
        self.assertNotEqual(block_to_block_type(invalid_quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        list_dash = "- Item 1\n- Item 2"
        
        self.assertEqual(block_to_block_type(list_dash), BlockType.UN_O_LIST)
        
        invalid_list = "- Item 1\n* Item 2"
        self.assertNotEqual(block_to_block_type(invalid_list), BlockType.UN_O_LIST) 

    def test_ordered_list(self):
        ordered_valid = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(ordered_valid), BlockType.O_LIST)
        
        ordered_invalid_start = "2. Second\n3. Third"
        self.assertNotEqual(block_to_block_type(ordered_invalid_start), BlockType.O_LIST)
        
        ordered_invalid_skip = "1. One\n3. Three"
        self.assertNotEqual(block_to_block_type(ordered_invalid_skip), BlockType.O_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is just plain text."), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("> Line 1\nLine 2 (breaks quote)"), BlockType.PARAGRAPH)
        
    def test_priority(self):
        self.assertEqual(block_to_block_type("> Test Quote"), BlockType.QUOTE)
        
        self.assertEqual(block_to_block_type("## Test Head"), BlockType.HEAD)
        
if __name__ == '__main__':
    unittest.main()