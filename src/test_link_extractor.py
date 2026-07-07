import unittest

from src.link_extractor import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image_link(self):
        text = "This contains ![a single image link](www.foo.bar)"
        output = extract_markdown_images(text)
        expeted = [("a single image link", "www.foo.bar")]
        self.assertEqual(output, expeted)

    def test_multiple_image_links(self):
        text = "This contains ![an image link](www.foo.bar) and ![another image link](www.boo.baz)"
        output = extract_markdown_images(text)
        expeted = [
            ("an image link", "www.foo.bar"),
            ("another image link", "www.boo.baz"),
        ]
        self.assertEqual(output, expeted)

    def test_no_image_links(self):
        text = "This is not what you are looking for..."
        output = extract_markdown_images(text)
        expeted = []
        self.assertEqual(output, expeted)

    def test_incorrect_image_pattern(self):
        text = "This contains [a normal link](www.foo.bar)"
        output = extract_markdown_images(text)
        expeted = []
        self.assertEqual(output, expeted)

    def test_mixed_images_and_links(self):
        text = "Text with ![an image](img.png) and [a link](link.com)"
        output = extract_markdown_images(text)
        self.assertEqual(output, [("an image", "img.png")])

    def test_adjacent_image_and_link(self):
        text = "![image](img.png)[link](link.com)"
        output = extract_markdown_images(text)
        self.assertEqual(output, [("image", "img.png")])

    def test_empty_alt_text(self):
        text = "![](www.foo.bar)"
        output = extract_markdown_images(text)
        self.assertEqual(output, [("", "www.foo.bar")])

    def test_empty_url(self):
        text = "![alt]()"
        output = extract_markdown_images(text)
        self.assertEqual(output, [("alt", "")])

    def test_empty_string(self):
        output = extract_markdown_images("")
        self.assertEqual(output, [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "This contains [a single link](www.foo.bar)"
        output = extract_markdown_links(text)
        expeted = [("a single link", "www.foo.bar")]
        self.assertEqual(output, expeted)

    def test_multiple_links(self):
        text = "This contains [a link](www.foo.bar) and [another link](www.boo.baz)"
        output = extract_markdown_links(text)
        expeted = [
            ("a link", "www.foo.bar"),
            ("another link", "www.boo.baz"),
        ]
        self.assertEqual(output, expeted)

    def test_no_image_links(self):
        text = "This is not what you are looking for..."
        output = extract_markdown_links(text)
        expeted = []
        self.assertEqual(output, expeted)

    def test_incorrect_image_pattern(self):
        text = "This contains ![an image link](www.foo.bar)"
        output = extract_markdown_links(text)
        expeted = []
        self.assertEqual(output, expeted)

    def test_mixed_images_and_links(self):
        text = "Text with ![an image](img.png) and [a link](link.com)"
        output = extract_markdown_links(text)
        self.assertEqual(output, [("a link", "link.com")])

    def test_adjacent_image_and_link(self):
        text = "![image](img.png)[link](link.com)"
        output = extract_markdown_links(text)
        self.assertEqual(output, [("link", "link.com")])

    def test_empty_anchor_text(self):
        text = "[](www.foo.bar)"
        output = extract_markdown_links(text)
        self.assertEqual(output, [("", "www.foo.bar")])

    def test_empty_url(self):
        text = "[text]()"
        output = extract_markdown_links(text)
        self.assertEqual(output, [("text", "")])

    def test_empty_string(self):
        output = extract_markdown_links("")
        self.assertEqual(output, [])
