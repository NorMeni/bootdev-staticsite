import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from gencontent import extract_title

class TestTextNode(unittest.TestCase):
	def test_extraction(self):
		self.assertEqual(extract_title("tests/yes_h1.md"), "Title is here.")

	def test_extraction2(self):
		with self.assertRaises(Exception) as cm:
			extract_title("tests/no_h1.md")
		self.assertIn("h1 header not found", str(cm.exception))


if __name__ == "__main__":
        unittest.main()
