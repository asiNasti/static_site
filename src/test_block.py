import unittest
from block import BlockType
from block import block_to_block_type, markdown_to_blocks, markdown_to_html_node

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

    def test_code(self):
        md_block = """
```
print("Hello, world!")
```
"""
        self.assertEqual(block_to_block_type(md_block), BlockType.CODE)
        
    def test_priority(self):
        self.assertEqual(block_to_block_type("> Test Quote"), BlockType.QUOTE)
        
        self.assertEqual(block_to_block_type("## Test Head"), BlockType.HEAD)



    class TestBlocksToHTML(unittest.TestCase):
        def test_paragraphs(self):
            md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>")


        def test_codeblock(self):
            md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html,
                "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>")
        
        def test_headings_and_paragraph(self):
            # Перевірка різних рівнів заголовків та їх змішування з параграфом
            md = """
# Heading 1

This is a paragraph under the heading.

## Heading 2 with **bold** text

### H3
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html,
                "<div><h1>Heading 1</h1><p>This is a paragraph under the heading.</p><h2>Heading 2 with <b>bold</b> text</h2><h3>H3</h3></div>")

        def test_quote_block(self):
            md = """
> This is a quote.
> It can span multiple lines.
> And include *italic* text.
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html,
                "<div><blockquote>This is a quote. It can span multiple lines. And include <i>italic</i> text.</blockquote></div>")

        def test_unordered_list(self):
            md = """
* First item
- Second item with `code`
* Third item
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html,
                "<div><ul><li>First item</li><li>Second item with <code>code</code></li><li>Third item</li></ul></div>")

        def test_ordered_list(self):
            md = """
1. Alpha
2. Beta with **bold** text
3. Gamma
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html,
                "<div><ol><li>Alpha</li><li>Beta with <b>bold</b> text</li><li>Gamma</li></ol></div>")

        def test_all_block_types_combined(self):
            md = """
# Main Title

> This is a quote.

* List item.

1. Ordered item.

```python
x = 1
```
A final paragraph.
"""
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html,
            "<div><h1>Main Title</h1><blockquote>This is a quote.</blockquote>"
            "<ul><li>List item.</li></ul><ol><li>Ordered item.</li></ol>"
            "<pre><code>x = 1\n</code></pre><p>A final paragraph.</p></div>")

if __name__ == '__main__':
    unittest.main()