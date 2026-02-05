import unittest
from block_parsing import markdown_to_blocks, block_to_blocktype, BlockType

class TestBlockParsing(unittest.TestCase):

    # -------------------------
    # markdown_to_blocks tests
    # -------------------------
    def test_basic_paragraph_split(self):
        md = "Hello\n\nWorld"
        self.assertListEqual(markdown_to_blocks(md), ["Hello", "World"])

    def test_extra_newlines_and_spaces(self):
        md = "\n\nHello\n\n\nWorld\n\n  "
        self.assertListEqual(markdown_to_blocks(md), ["Hello", "World"])

    def test_whitespace_only_blocks_removed(self):
        md = "Hello\n\n   \n\nWorld"
        self.assertListEqual(markdown_to_blocks(md), ["Hello", "World"])

    # -------------------------
    # block_to_blocktype tests
    # -------------------------
    def test_heading(self):
        self.assertEqual(block_to_blocktype("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_blocktype("## Heading 2"), BlockType.HEADING)

    def test_code_block(self):
        code_block = "```\nprint('Hello')\n```"
        self.assertEqual(block_to_blocktype(code_block), BlockType.CODE)
        # With language specifier
        code_block_lang = "```\npython\nprint('Hi')\n```"
        self.assertEqual(block_to_blocktype(code_block_lang), BlockType.CODE)

    def test_quote_block(self):
        quote = "> Line 1\n> Line 2"
        self.assertEqual(block_to_blocktype(quote), BlockType.QUOTE)

    def test_unordered_list_block(self):
        ul = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_blocktype(ul), BlockType.UNORDERED_LIST)

    def test_ordered_list_block(self):
        ol = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_blocktype(ol), BlockType.ORDERED_LIST)

    def test_paragraph_fallback(self):
        text = "Just a simple paragraph."
        self.assertEqual(block_to_blocktype(text), BlockType.PARAGRAPH)

    def test_empty_lines_do_not_break_lists(self):
        ul = "- item 1\n\n- item 2"
        self.assertEqual(block_to_blocktype(ul), BlockType.UNORDERED_LIST)

        ol = "1. first\n\n2. second"
        self.assertEqual(block_to_blocktype(ol), BlockType.ORDERED_LIST)

if __name__ == "__main__":
    unittest.main()
