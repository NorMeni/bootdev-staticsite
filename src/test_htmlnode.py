import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestTextNode(unittest.TestCase):
	def test_props_to_html(self):
		node = HTMLNode("p", "sample text", None, {"href": "https://www.google.com", "target": "_blank",})
		output = node.props_to_html()
		self.assertIn(' href="https://www.google.com"', output, "Props test 1 failed.")
		self.assertIn(' target="_blank"', output, "Props test 1 failed.")

	def test_props_to_html2(self):
		node = HTMLNode("p", "sample text", None, None)
		self.assertEqual(node.props_to_html(), "", "Props test 2 failed.")

	def test_props_to_html3(self):
		node = HTMLNode("p", "sample text", None, {"href": "https://www.google.com",})
		self.assertEqual(node.props_to_html(), ' href="https://www.google.com"', "Props test 3 failed.")

	def test_props_to_html4(self):
		node = HTMLNode("p", "sample text", None, {})
		self.assertEqual(node.props_to_html(), "", "Props test 4 failed.")

	def test_leaf_to_html(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>", "Leaf test 1 failed.")

	def test_leaf_to_html2(self):
		node = LeafNode("a", "Image link", {"href": "https://www.google.com"})
		self.assertEqual(node.to_html(), '<a href="https://www.google.com">Image link</a>', "Leaf test 2 failed.")

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>", "Failed to_html_with_children")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
			"Failed to_html_with_grandchildren",
		)

	def test_to_html_with_multiple_children(self):
		c1 = LeafNode("span", "a")
		c2 = LeafNode(None, "b")
		parent = ParentNode("div", [c1, c2], {"class": "box", "data-x": "1"})
		self.assertEqual(parent.to_html(), '<div class="box" data-x="1"><span>a</span>b</div>', "Failed multiple_children test.")

	def test_to_html_deep_nesting(self):
		g1 = LeafNode("i", "x")
		c1 = ParentNode("p", [LeafNode(None, "hi "), g1])
		c2 = LeafNode("b", "y")
		root = ParentNode("div", [c1, c2])
		self.assertEqual(root.to_html(), "<div><p>hi <i>x</i></p><b>y</b></div>", "Failed deep_nesting test.")

	def test_to_html_empty_children(self):
		parent = ParentNode("section", [])
		self.assertEqual(parent.to_html(), "<section></section>", "Failed empty_children test.")

if __name__ == "__main__":
	unittest.main()
