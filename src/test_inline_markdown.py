import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

example_text = [TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)]
broken_node = [TextNode("This is `broken markdown", TextType.TEXT)]
test_result = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("bolded phrase", TextType.BOLD),
    TextNode(" in the middle", TextType.TEXT),
]
start_text = [TextNode("`code` at the start", TextType.TEXT)]
test_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
test_nodes = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
one_type_result = [
    TextNode("this only has ", TextType.TEXT),
    TextNode("bold", TextType.BOLD),
    TextNode(" text", TextType.TEXT),
]
double_result = [
    TextNode("this has ", TextType.TEXT),
    TextNode("double", TextType.ITALIC),
    TextNode(" the ", TextType.TEXT),
    TextNode("italics", TextType.ITALIC)
]

class TestSplitDelimiter(unittest.TestCase):
    def test_broken_markdown(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter(broken_node, "`", TextType.CODE)
    def test_bold(self):
        bold_split = split_nodes_delimiter(example_text, "**", TextType.BOLD)
        self.assertEqual(bold_split, test_result)
    def test_delimiter_at_start(self):
        nodes = split_nodes_delimiter(start_text, "`", TextType.CODE)
        self.assertEqual(nodes, [TextNode("code", TextType.CODE), TextNode(" at the start", TextType.TEXT)])

class TestRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a [link](https://www.boot.dev/dashboard)")
        self.assertListEqual([("link", "https://www.boot.dev/dashboard")], matches)

class TestImageLinkMarkdown(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

class TestTextToTextNode(unittest.TestCase):
    def test_all_types(self):
        node = text_to_textnodes(test_text)
        self.assertEqual(node, test_nodes)
    def test_normal_text(self):
        node = text_to_textnodes("this is normal text")
        self.assertEqual(node, [TextNode("this is normal text", TextType.TEXT)])
    def test_one_type(self):
        node = text_to_textnodes("this only has **bold** text")
        self.assertEqual(node, one_type_result)
    def test_repeat_type(self):
        node = text_to_textnodes("this has _double_ the _italics_")
        self.assertEqual(node, double_result)
    def test_empty(self):
        node = text_to_textnodes("")
        self.assertEqual(node, [])

if __name__ == "__main__":
    unittest.main()