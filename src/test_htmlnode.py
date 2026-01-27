import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_parent_node(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
