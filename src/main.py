import os
import shutil
import sys
from generator import copy_dir, generate_pages_recursive

def main():
    try:
        basepath = sys.argv[1]
    except IndexError:
        basepath = '/'
    
    if not os.path.exists('static/'):
        raise Exception("not valid path")
    if os.path.exists('docs/'):
        shutil.rmtree('docs/')
    os.makedirs('docs', exist_ok=True)
    copy_dir('static/', 'docs/')

    dir_path_content = 'content/'
    template_path = 'template.html'
    dest_dir_path = 'docs/'
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath)
        
main()

if __name__ == "__main__":
    main()