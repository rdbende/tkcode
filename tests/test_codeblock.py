"""
A really simple test file for the most important features I need to test
"""

import unittest
from tkcode import CodeBlock


class TestCodeBlock(unittest.TestCase):
    def test_codeblock_init(self):
        widget = CodeBlock()
        widget.pack()

    def test_is_empty(self):
        widget = CodeBlock()
        self.assertTrue(widget.is_empty)
        self.assertEqual(widget.content, "\n")

    def test_content_change(self):
        widget = CodeBlock()
        widget.insert("end", "\n\n")
        self.assertEqual(widget.content, "\n\n\n")
        widget.content = "test"
        self.assertEqual(widget.content, "test\n")

    def test_line_numbers(self):
        widget = CodeBlock()
        widget.content = "\n\n"
        self.assertEqual(widget.number_of_lines, 3)


if __name__ == "__main__":
    unittest.main()
