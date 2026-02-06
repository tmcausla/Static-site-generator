from inline_parsing import text_to_textnodes
from textnode import *
from htmlnode import *
from block_parsing import *

def text_to_html_children(text):
    textnode_children = text_to_textnodes(text)
    return [text_node_to_html_node(child) for child in textnode_children]

def markdown_to_html_node(markdown):
    child_nodes = []
    md_blocks = markdown_to_blocks(markdown)
    for block in md_blocks:
        if block_to_blocktype(block) == BlockType.CODE:
            code_text = block[4:-3]
            code_textnode = TextNode(code_text, TextType.CODE)
            code_childnode = text_node_to_html_node(code_textnode)
            pre_parent = ParentNode("pre", [code_childnode])
            child_nodes.append(pre_parent)

        elif block_to_blocktype(block) == BlockType.HEADING:
            level = 0
            while level < len(block) and block[level] == "#":
                level += 1
            heading_text = block[level:].lstrip()
            inline_children = text_to_html_children(heading_text)
            h_parent = ParentNode(f"h{level}", inline_children)
            child_nodes.append(h_parent)

        elif block_to_blocktype(block) == BlockType.QUOTE:
            lines_of_quote = [line[1:].lstrip() for line in block.split('\n')]
            inline_children = text_to_html_children("\n".join(lines_of_quote))
            blockquote_parent = ParentNode("blockquote", inline_children)
            child_nodes.append(blockquote_parent)

        elif block_to_blocktype(block) == BlockType.UNORDERED_LIST:
            pass
            # strip "- " from each line
            # parse each line as children of <li>
            # add all <li> parents as children of <ul>
            # add <ul> parent to list of child_nodes

        elif block_to_blocktype(block) == BlockType.ORDERED_LIST:
            pass
            # strip "n. " from each line
            # parse each line as children of <li>
            # add all <li> parents as children of <ol>
            # add <ol> parent to list of child_nodes

        else: # else it's a PARAGRAPH block
            block_text = " ".join(block.split("\n"))
            inline_children = text_to_html_children(block_text)
            p_parent = ParentNode("p", inline_children)
            child_nodes.append(p_parent)
    return ParentNode("div", child_nodes)

test1 = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
test2 = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

test1_node = markdown_to_html_node(test1)
print(test1_node.to_html())
