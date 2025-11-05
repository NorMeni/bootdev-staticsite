import unittest

from textnode import *
from htmlnode import *
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

	def test_delimiter(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
		self.assertEqual(new_nodes,
		[
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("code block", TextType.CODE),
			TextNode(" word", TextType.TEXT),
		],
		"delimiter test failed.")

	def test_delimiter2(self):
		node = TextNode("This has **bold** and **more bold** text", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
		self.assertEqual(new_nodes, [
			TextNode("This has ", TextType.TEXT),
			TextNode("bold", TextType.BOLD),
			TextNode(" and ", TextType.TEXT),
			TextNode("more bold", TextType.BOLD),
			TextNode(" text", TextType.TEXT),
		])

	def test_delimiter3(self):
		node1 = TextNode("First `code` here", TextType.TEXT)
		node2 = TextNode("Second **bold** here", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
		self.assertEqual(new_nodes, [
			TextNode("First ", TextType.TEXT),
			TextNode("code", TextType.CODE),
			TextNode(" here", TextType.TEXT),
			TextNode("Second **bold** here", TextType.TEXT),
		])

	def test_delimiter4(self):
		node1 = TextNode("Already bold", TextType.BOLD)
		node2 = TextNode("Normal text with **bold**", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
		self.assertEqual(new_nodes, [
			TextNode("Already bold", TextType.BOLD),  # Unchanged
			TextNode("Normal text with ", TextType.TEXT),
			TextNode("bold", TextType.BOLD),
		])

	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_links(self):
		matches = extract_markdown_links(
			"This is my [first link](https://epicsite.com), and this is my [second one](https://google.com)"
		)
		self.assertListEqual([("first link", "https://epicsite.com"), ("second one", "https://google.com")], matches)

	def test_split_image(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
			],
			new_nodes,
		)

	def test_split_links(self):
		node = TextNode(
			"This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://boot.dev"),
				TextNode(" and ", TextType.TEXT),
				TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
				TextNode(" with text that follows", TextType.TEXT),
			],
			new_nodes,
		)

	def test_text_to_textnodes(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		new_nodes = text_to_textnodes(text)
		self.assertListEqual(
			[
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
			],
			new_nodes,
		)

	def test_markdown_to_blocks(self):
		md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""

		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is **bolded** paragraph",
				"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
				"- This is a list\n- with items",
			],
		)

	def test_blocktype(self):
		block = "### Hello world"
		self.assertEqual(block_to_block_type(block), BlockType.HEADING)

	def test_blocktype2(self):
		block = "1. first\n2. second\n3. third"
		self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

	def test_blocktype3(self):
		block = "> wisdom\n> from the forest"
		self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

	def test_paragraphs(self):
		md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
		)

	def test_codeblock(self):
		md = """```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
		)

if __name__ == "__main__":
	unittest.main()
