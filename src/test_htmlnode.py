import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

fake_prop = {
    "href": "https://www.google.com",
    "target": "_blank",
}

class TestHTMLNode(unittest.TestCase):
    def test_propnone(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(node.props_to_html(), "")
    def test_propanswer(self):
        node = HTMLNode(None, None, None, fake_prop)
        self.assertEqual(node.props_to_html(),  ' href="https://www.google.com" target="_blank"')
    def test_propempty(self):
        node = HTMLNode(None, None, None, {})
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "TestTest", fake_prop)
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">TestTest</a>')
    def test_leaf_empty_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_leaf_empty_tag(self):
        node = LeafNode(None, "TestTest")
        self.assertEqual(node.to_html(), "TestTest")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_great_grandchildren(self):
        leaf = LeafNode("b", "innermost text")
        inner_parent = ParentNode("span", [leaf])
        middle_parent = ParentNode("div", [inner_parent])
        outer_parent = ParentNode("section", [middle_parent])
    
        self.assertEqual(
            outer_parent.to_html(),
            "<section><div><span><b>innermost text</b></span></div></section>"
        )

    def test_to_html_mixed_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                ParentNode("span", [LeafNode("i", "italicized")]),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold</b><span><i>italicized</i></span>Normal text</p>"
        )

    def test_to_html_parent_with_props(self):
        child = LeafNode("p", "paragraph")
        parent = ParentNode("div", [child], {"class": "main-container", "id": "main"})
    
        self.assertEqual(
            parent.to_html(),
            '<div class="main-container" id="main"><p>paragraph</p></div>'
        )

if __name__ == "__main__":
    unittest.main()