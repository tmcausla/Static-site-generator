from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

TEXT_TAGS = {
    TextType.BOLD: "b",
    TextType.ITALIC: "i",
    TextType.CODE: "code"
}

class TextNode:
    def __init__(self, text, text_type, url=None):
        if text_type in { TextType.LINK, TextType.IMAGE } and not url:
            raise ValueError(f"{text_type.value} nodes require a url")
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        output = f'TextNode("{self.text}", {self.text_type.value}'
        if self.url:
            output += f', "{self.url}")'
        else:
            output += ")"
        return output


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type in TEXT_TAGS:
        return LeafNode(TEXT_TAGS[text_node.text_type], text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode('a', text_node.text, { "href": text_node.url })
    if text_node.text_type == TextType.IMAGE:
        return LeafNode('img', "", { "src": text_node.url, "alt": text_node.text })
    raise ValueError(f"unsupported TextType: {text_node.text_type}")
