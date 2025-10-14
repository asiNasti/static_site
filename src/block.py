from enum import Enum
import re

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
    
    match_code = re.match(r"^\`\`\`.+\`\`\`$", block)
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
