import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("would-be italic text", TextType.ITALIC)
        node2 = TextNode("would-be italic text", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("something from a url", TextType.LINK, "https://haha.gotcha")
        node2 = TextNode("something from a url", TextType.LINK, "https://haha.gotcha")
        node3 = TextNode("something from a url", TextType.IMAGE, "https://haha.gotcha")
        node4 = TextNode("something from a url", TextType.BOLD)
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_to_leafnode(self):
        node = TextNode("Here be linx", TextType.LINK, "https://dagoogs.ca")
        html_node = text_node_to_html_node(node)
        self.assertEqual(repr(html_node), "LeafNode(a, Here be linx, {'href': 'https://dagoogs.ca'})")

    def test_image_to_leafnode(self):
        node = TextNode("An image of magi", TextType.IMAGE, "www.wowmagic.gov")
        html_node = text_node_to_html_node(node)
        self.assertEqual(repr(html_node), "LeafNode(img, , {'src': 'www.wowmagic.gov', 'alt': 'An image of magi'})")

if __name__ == "__main__":
    unittest.main()
