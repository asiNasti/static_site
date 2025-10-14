from textnode import TextNode
def main():
    text = 'This is some anchor text'
    text_type = 'link'
    url = 'https://www.boot.dev'
    textnode = TextNode(text, text_type, url)
    print(textnode)

main()