import unittest
from textnode import TextNode, TextType
from inline_parsing import *
from block_parsing import *

class TestMarkdownSplitting(unittest.TestCase):

    # -------------------------
    # IMAGE TEST CASES
    # -------------------------
    def test_single_image(self):
        node = TextNode("Here is an ![img](https://example.com/img.png)!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is an ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://example.com/img.png"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes
        )

    def test_image_at_start(self):
        node = TextNode("![start](https://example.com/start.png) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes
        )

    def test_image_at_end(self):
        node = TextNode("Text before ![end](https://example.com/end.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes
        )

    def test_consecutive_images(self):
        node = TextNode("![a](https://example.com/a.png)![b](https://example.com/b.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://example.com/a.png"),
                TextNode("b", TextType.IMAGE, "https://example.com/b.png"),
            ],
            new_nodes
        )

    def test_no_images(self):
        node = TextNode("Just some plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    # -------------------------
    # LINK TEST CASES
    # -------------------------
    def test_single_link(self):
        node = TextNode("Click [here](https://example.com) now", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://example.com"),
                TextNode(" now", TextType.TEXT),
            ],
            new_nodes
        )

    def test_link_at_start(self):
        node = TextNode("[start](https://example.com) followed by text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.LINK, "https://example.com"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes
        )

    def test_link_at_end(self):
        node = TextNode("Text before [end](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("end", TextType.LINK, "https://example.com"),
            ],
            new_nodes
        )

    def test_consecutive_links(self):
        node = TextNode("[a](https://example.com/a)[b](https://example.com/b)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "https://example.com/a"),
                TextNode("b", TextType.LINK, "https://example.com/b"),
            ],
            new_nodes
        )

    def test_no_links(self):
        node = TextNode("Just some plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **bold text** with an _italic_ word **and** a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word ", TextType.TEXT),
            TextNode("and", TextType.BOLD),
            TextNode(" a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(blocks, expected)

    def test_extra_spacing(self):
        md = "Hello\n\n\nWorld"
        blocks = markdown_to_blocks(md)
        expected = ["Hello", "World"]
        self.assertEqual(blocks, expected)

    def test_leading_trailing_newline(self):
        md = "\n\nHello\n\nWorld\n\n"
        blocks = markdown_to_blocks(md)
        expected = expected = ["Hello", "World"]
        self.assertEqual(blocks, expected)

    def test_whitespace_only_blocks(self):
        md = "Hello\n\n   \n\nWorld"
        blocks = markdown_to_blocks(md)
        expected = expected = ["Hello", "World"]
        self.assertEqual(blocks, expected)

if __name__ == "__main__":
    unittest.main()
