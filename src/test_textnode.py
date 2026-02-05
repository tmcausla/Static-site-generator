import unittest
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode
from markdown_splitting import *

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
        self.assertEqual(repr(html_node), "LeafNode(img,  , {'src': 'www.wowmagic.gov', 'alt': 'An image of magi'})")
        self.assertEqual(html_node.to_html(), '<img src="www.wowmagic.gov" alt="An image of magi" />')

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with _italic words at the end_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with ", TextType.TEXT), TextNode("italic words at the end", TextType.ITALIC)])

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("**Big bold words** in the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("Big bold words", TextType.BOLD), TextNode(" in the beginning", TextType.TEXT)])

    def test_multiple_italic_blocks(self):
        node = TextNode("_Italic here_ and another _italic here_ but not here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("Italic here", TextType.ITALIC), TextNode(" and another ", TextType.TEXT), TextNode("italic here", TextType.ITALIC), TextNode(" but not here", TextType.TEXT)])

    def test_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        image_list = extract_markdown_images(text)
        self.assertEqual(image_list, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        link_list = extract_markdown_links(text)
        self.assertEqual(link_list, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()
