from enum import Enum
from itertools import count
import re

from htmlnode import HTMLNode, ParentNode
from text_processing import text_to_textnodes, text_node_to_html_node
from textnode import TextType, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UN_O_LIST = "unordered_list"
    O_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    markdown = markdown.split("\n\n")
    for item in markdown:
        if item.strip() != "":
            blocks.append(item.strip())
    return blocks


def block_to_block_type(block):
    match_headings = re.match(r"^\#{1,6} .+", block)
    if match_headings:
        return BlockType.HEAD
    
    match_code = re.match(r"^\`\`\`.+\`\`\`$", block.strip(), re.DOTALL)
    if match_code:
        return BlockType.CODE

    lines = block.split("\n")
    quote = True
    for line in lines:
        match_quote = re.match(r"^\>", line)
        if not match_quote:
            quote = False
            break
    unordered = True
    for line in lines:
        match_unordered = re.match(r"^\-", line)
        if not match_unordered:
            unordered = False
            break
    ordered = True
    for i in range(len(lines)):
        if not lines[i].startswith(f"{i+1}. "):
            ordered = False
            break

    if quote:
        return BlockType.QUOTE
    elif unordered:
        return BlockType.UN_O_LIST
    elif ordered:
        return BlockType.O_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    block_nodes = text_to_textnodes(text)
    list_of_nodes = []
    for node in block_nodes:
        list_of_nodes.append(text_node_to_html_node(node))
    return list_of_nodes

def paragraph_block_to_html(block):
    clean_text = block.replace("\n", " ")
    children = text_to_children(clean_text)
    return ParentNode("p", children=children)

def heading_block_to_html(block):
    level = 0
    for i in range(len(block)):
        if block[i] == "#":
            level += 1
            continue
        break
    clean_text = block[level+1:].srtip()
    children = text_to_children(clean_text)
    return ParentNode(f"h{level}", children=children)

def quote_block_to_html(block):
    lines = block.split('\n')
    clean_lines = []
    for line in lines:
        if line.startswith(">"):
            clear_line = line[1:].strip()
        else:
            clear_line = line.strip()
        clean_lines.append(clear_line)
    clean_text = " ".join(clean_lines)
    children = text_to_children(clean_text)
    return ParentNode("blockquote", children=children)

def un_o_block_to_html(block):
    lines = block.split('\n')
    list_item_nodes = []
    for line in lines:
        clean_text = line[2:].strip()
        children_of_li = text_to_children(clean_text)
        li_node = ParentNode("li", children_of_li)
        list_item_nodes.append(li_node)
    return ParentNode("ul", children=list_item_nodes)

def o_block_to_html(block):
    lines = block.split('\n')
    list_item_nodes = []
    for line in lines:
        clean_text = line[2:].strip()
        children_of_li = text_to_children(clean_text)
        li_node = ParentNode("li", children_of_li)
        list_item_nodes.append(li_node)
    return ParentNode("ol", children=list_item_nodes)

def code_block_to_html(block):
    clean_text = block.strip("```").rstrip("```").strip()
    code_node = text_node_to_html_node(TextNode(clean_text, TextType.CODE))
    return ParentNode("pre", children=[code_node])


def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return paragraph_block_to_html(block)

    elif block_type == BlockType.HEAD:
        return heading_block_to_html(block)
        
    elif block_type == BlockType.QUOTE:
        return quote_block_to_html(block)
        
    elif block_type == BlockType.UN_O_LIST:
        return un_o_block_to_html(block)
        
    elif block_type == BlockType.O_LIST:
        return o_block_to_html(block)
        
    elif block_type == BlockType.CODE:
        return code_block_to_html(block)
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type) 
        block_nodes.append(html_node)

    return ParentNode(tag="div", children=block_nodes)