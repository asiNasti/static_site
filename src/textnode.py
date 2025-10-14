from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        

    def __eq__(self, another):
        return (self.text == another.text and 
                self.text_type == another.text_type and 
                self.url == another.url)
    

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'


def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise TypeError
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        prop = {"href": text_node.url}
        return LeafNode("a", text_node.text, prop)
    
    elif text_node.text_type == TextType.IMAGE:
        prop = {"src": text_node.url, "alt": text_node.text}
        return LeafNode("img", '', prop)
        