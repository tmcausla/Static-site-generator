import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()
