from textnode import TextNode, TextType

def main():
    test1 = TextNode("This is some anchor text", TextType.LINK, "https://example.com")
    test2 = TextNode("This will be plain text", TextType.TEXT)
    test3 = TextNode("An image of magi", TextType.IMAGE, "www.magiimages.we")
    print(test1)
    print(test2)
    print(test3)

main()
