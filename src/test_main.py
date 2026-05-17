import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_strips_whitespace(self):
        markdown = "#     Hello there     "
        self.assertEqual(extract_title(markdown), "Hello there")

    def test_extract_title_ignores_other_headings(self):
        markdown = """
## Not the title

# Real title
"""
        self.assertEqual(extract_title(markdown), "Real title")

    def test_extract_title_raises_when_missing(self):
        markdown = """
## Subtitle

Paragraph text
"""
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
