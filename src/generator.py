import os
import shutil

from block import markdown_to_html_node


def copy_dir(source, destiny):
    elements_in_source = os.listdir(source)
    for item in elements_in_source:
        path_to_item = os.path.join(source, item)
        if os.path.isfile(path_to_item):
            shutil.copy(path_to_item, destiny)
        else:
            path_to_dir = os.path.join(destiny, item)
            os.mkdir(path_to_dir)
            copy_dir(path_to_item, path_to_dir)


def extract_title(markdown):
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block.strip().startswith("# "):
            clean_block = block.replace("# ", "", 1).strip()
            return clean_block
    raise Exception('there is no h1 header')
        

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as m:
        markdown = m.read()

    with open(template_path, "r") as t:
        template = t.read()

    node = markdown_to_html_node(markdown)
    html_text = node.to_html()
    title = extract_title(markdown)

    final_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_text)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)

    for item in os.listdir(dir_path_content):
        path_to_item = os.path.join(dir_path_content, item)
        path_to_dest = os.path.join(dest_dir_path, item)

        if os.path.isfile(path_to_item) and item.endswith(".md"):
            html_name = item.replace(".md", ".html")
            path_to_dest = os.path.join(dest_dir_path, html_name)
            generate_page(path_to_item, template_path, path_to_dest)

        elif os.path.isdir(path_to_item):
            generate_pages_recursive(path_to_item, template_path, path_to_dest)
