from inline_parsing import text_to_textnodes
from textnode import *
from htmlnode import LeafNode, ParentNode
from block_parsing import *

def text_to_html_children(text):
    textnode_children = text_to_textnodes(text)
    return [text_node_to_html_node(child) for child in textnode_children]

def markdown_to_html_node(markdown):
    child_nodes = []
    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        block_parent = None
        block_type = block_to_blocktype(block)
        if block_type == BlockType.CODE:
            code_text = block[4:-3]
            code_textnode = TextNode(code_text, TextType.CODE)
            code_childnode = text_node_to_html_node(code_textnode)
            block_parent = ParentNode("pre", [code_childnode])

        elif block_type == BlockType.HEADING:
            level = 0
            while level < len(block) and block[level] == "#":
                level += 1
            heading_text = block[level:].lstrip()
            inline_children = text_to_html_children(heading_text)
            block_parent = ParentNode(f"h{level}", inline_children)

        elif block_type == BlockType.QUOTE:
            lines_of_quote = [line[1:].lstrip() for line in block.split('\n')]
            quote_children = []
            for i, line in enumerate(lines_of_quote):
                quote_children.extend(text_to_html_children(line))
                if i < len(lines_of_quote) - 1:
                    quote_children.append(LeafNode("br", ""))
            block_parent = ParentNode("blockquote", quote_children)

        elif block_type == BlockType.UNORDERED_LIST:
            list_item_text = [line[2:].lstrip() for line in block.split('\n')]
            ul_children = []
            for line in list_item_text:
                inline_children = text_to_html_children(line)
                li_parent = ParentNode("li", inline_children)
                ul_children.append(li_parent)
            block_parent = ParentNode("ul", ul_children)

        elif block_type == BlockType.ORDERED_LIST:
            list_item_text = block.split('\n')
            ol_children = []
            for line in list_item_text:
                line = line.split(". ", 1)[1].lstrip()
                inline_children = text_to_html_children(line)
                li_parent = ParentNode("li", inline_children)
                ol_children.append(li_parent)
            block_parent = ParentNode("ol", ol_children)

        else: # invalid markdown defaults to PARAGRAPH block
            block_text = " ".join(block.split("\n"))
            inline_children = text_to_html_children(block_text)
            block_parent = ParentNode("p", inline_children)

        if block_parent is None:
            raise ValueError(f"unhandled blocktype: {block_type}")
        child_nodes.append(block_parent)
    return ParentNode("div", child_nodes)
