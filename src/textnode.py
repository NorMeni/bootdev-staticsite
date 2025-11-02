from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
	TEXT = ""
	BOLD = "b"
	ITALIC = "i"
	CODE = "code"
	LINK = "a"
	IMAGE = "img"

class TextNode:
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, node):
		if self.text == node.text and self.text_type == node.text_type and self.url == node.url:
			return True
		return False

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text, None)
		case TextType.BOLD:
			return LeafNode("b", text_node.text, None)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text, None)
		case TextType.CODE:
			return LeafNode("code", text_node.text, None)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
		case _:
			raise ValueError()
