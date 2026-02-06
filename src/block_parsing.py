from enum import Enum
from textnode import *
from inline_parsing import *
from htmlnode import *
import re

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    clean_blocks = [md.strip() for md in raw_blocks if md.strip()]
    return clean_blocks

def block_to_blocktype(block):
    lines_of_text = block.split("\n")

    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines_of_text if line.strip()):
        return BlockType.QUOTE

    if all(line.strip().startswith("- ") for line in lines_of_text if line.strip()):
        return BlockType.UNORDERED_LIST

    bullet = 1
    content_lines = [l for l in lines_of_text if l.strip()]
    for line in content_lines:
        if not line.strip().startswith(f"{bullet}. "):
            break
        bullet += 1
    if bullet == len(content_lines) + 1:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
