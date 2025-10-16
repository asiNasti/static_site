import os
import shutil
from generator import copy_dir, generate_pages_recursive

def main():
    if not os.path.exists('static/'):
        raise Exception("not valid path")
    if os.path.exists('public/'):
        shutil.rmtree('public/')
    os.mkdir('public/')
    copy_dir('static/', 'public/')

    dir_path_content = 'content/'
    template_path = 'template.html'
    dest_dir_path = 'public/'
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)
        
main()