import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_typenoneq(self):
        node = TextNode("This text is same", TextType.TEXT)
        node2 = TextNode("This text is same", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_urlnone(self):
        node = TextNode("text here", TextType.TEXT, None)
        node2 = TextNode("text here", TextType.TEXT)
        self.assertEqual(node, node2)
    def test_textnoneq(self):
        node = TextNode("This text is different", TextType.TEXT)
        node2 = TextNode("This text is very different", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()