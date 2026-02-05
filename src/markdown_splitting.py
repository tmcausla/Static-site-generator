from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_node_text = node.text.split(delimiter)
        if len(split_node_text) == 1:
            new_nodes.append(node)
        elif len(split_node_text) % 2 == 0:
            raise Exception("delimiter error: invalid markdown syntax.  formatted section not closed")
        else:
            for i in range(len(split_node_text)):
                if not split_node_text[i]:
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_node_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_node_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    regex = r"!\[([^\[\]]+)\]\(([^\(\)]+)\)"
    image_list = re.findall(regex, text)
    return image_list

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        image_list = extract_markdown_images(node.text)
        if not image_list:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt, url in image_list:
            image_markdown = f"![{alt}]({url})"
            before, _, remaining_text = remaining_text.partition(image_markdown)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def extract_markdown_links(text):
    regex = r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)"
    link_list = re.findall(regex, text)
    return link_list

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        link_list = extract_markdown_links(node.text)
        if not link_list:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for text, url in link_list:
            link_markdown = f"[{text}]({url})"
            before, _, remaining_text = remaining_text.partition(link_markdown)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(text, TextType.LINK, url))

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    raw_node = TextNode(text, TextType.TEXT)

    after_bold = split_nodes_delimiter([raw_node], "**", TextType.BOLD)
    after_italic = split_nodes_delimiter(after_bold, "_", TextType.ITALIC)
    after_code = split_nodes_delimiter(after_italic, "`", TextType.CODE)
    after_images = split_nodes_image(after_code)
    after_links = split_nodes_link(after_images)

    return after_links

