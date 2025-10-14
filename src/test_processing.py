import unittest

from text_processing import text_node_to_html_node, split_nodes_delimiter
from text_processing import extract_markdown_images, extract_markdown_links
from text_processing import split_nodes_image, split_nodes_link, text_to_textnodes

from textnode import TextType, TextNode

class TestNodeToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("this is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "this is bold")

    def test_code(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_link(self):
        node = TextNode("url", TextType.LINK, "https://google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://google.com"})

    def test_image(self):
        node = TextNode("img description", TextType.IMAGE, "/img/photo.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "/img/photo.png", "alt": "img description"})

    def test_exception_unknown_type(self):
        node = TextNode("unknown", "unknown_type") 
        with self.assertRaises(TypeError):
            text_node_to_html_node(node)

class TestSplitNodesText(unittest.TestCase):
    def test_simple(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)

        expected_output = [TextNode("This is text with a ", TextType.TEXT), 
                           TextNode("code block", TextType.CODE), 
                           TextNode(" word", TextType.TEXT)]
        
        actual_output = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(expected_output, actual_output)

    def test_multiple_delimiter_splits(self):
        node = TextNode("Text **bold** and another **one** block.", TextType.TEXT)

        expected_nodes = [TextNode("Text ", TextType.TEXT), 
                          TextNode("bold", TextType.BOLD),
                          TextNode(" and another ", TextType.TEXT),
                          TextNode("one", TextType.BOLD),
                          TextNode(" block.", TextType.TEXT)]
        
        actual_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_start_and_end_with_delimiter(self):
        node = TextNode("_Italic text_", TextType.TEXT)
        expected_nodes = [TextNode("Italic text", TextType.ITALIC)]
        actual_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_handles_non_text(self):
        non_text_node = TextNode("https://example.com", TextType.LINK, "https://example.com")
        text_node = TextNode("Regular `code text`.", TextType.TEXT)
        
        expected_nodes = [non_text_node,
                          TextNode("Regular ", TextType.TEXT),
                          TextNode("code text", TextType.CODE),
                          TextNode(".", TextType.TEXT)]
        
        actual_nodes = split_nodes_delimiter([non_text_node, text_node], "`", TextType.CODE)
        self.assertEqual(actual_nodes, expected_nodes)

    def test_unclosed_delimiter(self):
        node = TextNode("Text with **one delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        actual_nodes = extract_markdown_images(text)
        expected_nodes = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
                          ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(actual_nodes, expected_nodes)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        actual_nodes = extract_markdown_links(text)
        expected_nodes = [("to boot dev", "https://www.boot.dev"), 
                          ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(actual_nodes, expected_nodes)


class TestSplitNodesImageLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,)
        
        actual_nodes = split_nodes_image([node])
        expected_nodes = [TextNode("This is text with an ", TextType.TEXT),
                          TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                          TextNode(" and another ", TextType.TEXT),
                          TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")]
        
        self.assertListEqual(actual_nodes, expected_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,)
        
        actual_nodes = split_nodes_link([node])
        expected_nodes = [TextNode("This is text with a link ", TextType.TEXT),
                          TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                          TextNode(" and ", TextType.TEXT),
                          TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")]
        
        self.assertListEqual(actual_nodes, expected_nodes)

class TestTextToNodes(unittest.TestCase):
    def test_full(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        actual_nodes = text_to_textnodes(text)
        expected_nodes = [TextNode("This is ", TextType.TEXT),
                          TextNode("text", TextType.BOLD),
                          TextNode(" with an ", TextType.TEXT),
                          TextNode("italic", TextType.ITALIC),
                          TextNode(" word and a ", TextType.TEXT),
                          TextNode("code block", TextType.CODE),
                          TextNode(" and an ", TextType.TEXT),
                          TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                          TextNode(" and a ", TextType.TEXT),
                          TextNode("link", TextType.LINK, "https://boot.dev")]
        
        self.assertListEqual(actual_nodes, expected_nodes)


if __name__ == "__main__":
    unittest.main()