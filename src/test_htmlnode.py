import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"}
        )

        expected_output = ' href="https://google.com" target="_blank"'
        actual_output = node.props_to_html()

        self.assertEqual(expected_output, actual_output)

    def test_props_to_html_none(self):
        node = HTMLNode()

        expected_output = ""
        actual_output = node.props_to_html()

        self.assertEqual(expected_output, actual_output)

    def test_repr_full(self):
        node = HTMLNode(tag="p",
            value="This is a text node",
            children=[HTMLNode(tag="b", value="bold")],
            props={"class": "main", "id": "p1"})
        
        expected_output = ("HTMLNode(p, This is a text node, "
            "[HTMLNode(b, bold, None, None)], "
            "{'class': 'main', 'id': 'p1'})")
        actual_output = repr(node) 

        self.assertEqual(expected_output, actual_output)
    
    def test_repr_none(self):
        node = HTMLNode(tag="br")
        
        expected_output = 'HTMLNode(br, None, None, None)'
        actual_output = repr(node) 

        self.assertEqual(expected_output, actual_output)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is bold text.")
        self.assertEqual(node.to_html(), "<b>This is bold text.</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected_output = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected_output)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()