import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TextTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2, "First eq test failed.")

	def test_not_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD, "google") 
		self.assertNotEqual(node, node2, "First not_eq test failed.")

	def test_not_eq2(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node3 = TextNode("This is a text node", TextType.CODE)
		self.assertNotEqual(node, node3, "Second not_eq test failed.")

	def test_not_eq3(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node4 = TextNode("This is a text node 2", TextType.BOLD)
		self.assertNotEqual(node, node4, "Third not_eq test failed.")

	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None, "test_text failed.")
		self.assertEqual(html_node.value, "This is a text node", "test_text failed.")

if __name__ == "__main__":
	unittest.main()
