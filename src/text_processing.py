import re

from textnode import TextType, TextNode, LeafNode

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
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)

        elif node.text_type is TextType.TEXT:
            node_parts = node.text.split(delimiter)
            if len(node_parts) % 2 == 0:
                raise Exception("that's invalid Markdown syntax")
            
            for i in range(len(node_parts)):
                if i % 2 == 0 and len(node_parts[i]) != 0:
                    new_nodes.append(TextNode(node_parts[i], TextType.TEXT))
                elif i % 2 != 0 and len(node_parts[i]) != 0:
                    new_nodes.append(TextNode(node_parts[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    images = []
    match_alt_text = re.findall(r"!\[.*?\]", text)
    match_url = re.findall(r"\(.*?\)", text)
    for i in range(len(match_alt_text)):
        images.append((match_alt_text[i].strip("![").rstrip("]"), match_url[i].strip("(").rstrip(")")))
    return images


def extract_markdown_links(text):
    links = []
    match_anchor_text = re.findall(r"\[.*?\]", text)
    match_url = re.findall(r"\(.*?\)", text)
    for i in range(len(match_anchor_text)):
        links.append((match_anchor_text[i].strip("[").rstrip("]"), match_url[i].strip("(").rstrip(")")))
    return links


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)

        elif node.text_type is TextType.TEXT:
            matches = extract_markdown_images(node.text)
            if not matches:
                new_nodes.append(node)
                continue
            
            current_text = node.text
            for image_alt, image_link in matches:
                node_parts = current_text.split(f"![{image_alt}]({image_link})", 1)

                if len(node_parts) != 2:
                    raise Exception("that's invalid Markdown syntax")
                
                if node_parts[0] != "":
                    new_nodes.append(TextNode(node_parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

                current_text = node_parts[1]

            if current_text != "":
                new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)

        elif node.text_type is TextType.TEXT:
            matches = extract_markdown_links(node.text)
            if not matches:
                new_nodes.append(node)
                continue
            
            current_text = node.text
            for anchor_text, url in matches:
                node_parts = current_text.split(f"[{anchor_text}]({url})", 1)

                if len(node_parts) != 2:
                    raise Exception("that's invalid Markdown syntax")
                
                if node_parts[0] != "":
                    new_nodes.append(TextNode(node_parts[0], TextType.TEXT))
                new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

                current_text = node_parts[1]

            if current_text != "":
                new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes
