import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode('a', "some kinda link", None, { "href": "https://www.google.com", "target": "_blank" })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_stringify(self):
        node = HTMLNode('div', None, ["p", "a", "img"], { "class": "classi" })
        self.assertEqual(repr(node), "HTMLNode(div, None, ['p', 'a', 'img'], {'class': 'classi'})")

    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_link_to_html(self):
        node = LeafNode("a", "some kinda link", { "href": "https://www.google.com", "target": "_blank" })
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">some kinda link</a>')

    def test_leaf_string(self):
        node = LeafNode("p", "run of the mill text", { "id": "teste" })
        self.assertEqual(repr(node), "LeafNode(p, run of the mill text, {'id': 'teste'})")
