from enum import Enum, auto
from htmlnode import LeafNode, HTMLNode
import re

class TextType(Enum):
	TEXT = ""
	BOLD = "b"
	ITALIC = "i"
	CODE = "code"
	LINK = "a"
	IMAGE = "img"

class BlockType(Enum):
	PARAGRAPH = auto()
	HEADING = auto()
	CODE = auto()
	QUOTE = auto()
	UNORDERED_LIST = auto()
	ORDERED_LIST = auto()

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	result = []

	for node in old_nodes:
		new_nodes = []
		if node.text_type != TextType.TEXT:
			result.append(node)
			continue
		if node.text.count(delimiter) % 2 == 1:
			raise Exception("Invalid Markdown Syntax")
		if delimiter not in node.text:
			result.append(node)
			continue

		split_string = node.text.split(delimiter)
		for i in range(0, len(split_string)):
			if split_string[i] == "":
				continue
			if i % 2 == 0:
				result.append(TextNode(split_string[i], TextType.TEXT))
			else:
				result.append(TextNode(split_string[i], text_type))
	return result

def split_nodes_image(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		original_text = old_node.text
		images = extract_markdown_images(original_text)
		if len(images) == 0:
			new_nodes.append(old_node)
			continue
		for image in images:
			sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
			if len(sections) != 2:
				raise ValueError(f"invalid markdown, image section not closed")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], TextType.TEXT))
			new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
			original_text = sections[1]
		if original_text != "":
			new_nodes.append(TextNode(original_text, TextType.TEXT))
	return new_nodes

def split_nodes_link(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			new_nodes.append(old_node)
			continue
		original_text = old_node.text
		links = extract_markdown_links(original_text)
		if len(links) == 0:
			new_nodes.append(old_node)
			continue
		for link in links:
			sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
			if len(sections) != 2:
				raise ValueError("invalid markdown, link section not closed")
			if sections[0] != "":
				new_nodes.append(TextNode(sections[0], TextType.TEXT))
			new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
			original_text = sections[1]
		if original_text != "":
			new_nodes.append(TextNode(original_text, TextType.TEXT))
	return new_nodes

def extract_markdown_images(text):
	matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def extract_markdown_links(text):
	matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
	return matches

def text_to_textnodes(text):
	first_round = [TextNode(text, TextType.TEXT)]
	second_round = split_nodes_delimiter(first_round, "`", TextType.CODE)
	third_round = split_nodes_image(second_round)
	fourth_round = split_nodes_link(third_round)
	fifth_round = split_nodes_delimiter(fourth_round, "**", TextType.BOLD)
	return split_nodes_delimiter(fifth_round, "_", TextType.ITALIC)

def markdown_to_blocks(markdown):
	current = []
	blocks = []
	current_kind = None

	for raw in markdown.splitlines():
		line = raw.rstrip("\n")
		if line.strip() == "":
			if current:
				blocks.append("\n".join(current))
				current = []
				current_kind = None
			continue

		line_kind = "quote" if line.lstrip().startswith(">") else "para"

		if current_kind in (None, line_kind):
			current.append(line)
			current_kind = line_kind
		else:
			blocks.append("\n".join(current))
			current = [line]
			current_kind = line_kind
	if current:
		blocks.append("\n".join(current))
	#print(repr(blocks))
	return blocks

def block_to_block_type(markdown):
	#check code
	lines = markdown.strip().splitlines()
	if len(lines) >= 2 and lines[0].strip() == "```" and lines[-1].strip() == "```":
		return BlockType.CODE

	#check heading
	m = re.match(r"^(#{1,6})\s+(\S.*)$", markdown)
	if m:
		return BlockType.HEADING

	#check unordered and quote
	lines_list = markdown.split("\n")
	first = next((ln for ln in lines_list if ln.strip() != ""), "")
	if first.lstrip().startswith(">"):
		for ln in lines_list:
			if ln.strip() == "":
				continue
			s = ln.lstrip()
			if not s.startswith(">"):
				return BlockType.PARAGRAPH
		return BlockType.QUOTE
	elif first.lstrip().startswith("- "):
		for ln in lines_list:
			if ln.strip() == "":
				continue
			if not ln.lstrip().startswith("- "):
				return BlockType.PARAGRAPH
		return BlockType.UNORDERED_LIST
	#check ordered list
	if markdown.startswith("1. "):
		lines = markdown.split("\n")
		for idx, line in enumerate(lines, start=1):
			prefix = f"{idx}. "
			if not line.startswith(prefix):
				return BlockType.PARAGRAPH
			if len(line) <= len(prefix):
				return BlockType.PARAGRAPH
		return BlockType.ORDERED_LIST
	return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	node_list = []
	for text in blocks:
		type = block_to_block_type(text)
		match type:
			case BlockType.CODE:
				lines = text.strip().splitlines()
				if len(lines) >= 2 and lines[0].strip() == "```" and lines[-1].strip() == "```":
					inner = "\n".join(lines[1:-1]) + "\n"
					norm = TextNode(inner, TextType.TEXT)
					leaf_children = [text_node_to_html_node(norm)]
					leaf_node = HTMLNode("code", None, leaf_children)
					p_node = HTMLNode("pre", None, [leaf_node])
					node_list.append(p_node)
				else: continue
			case BlockType.HEADING:
				m = re.match(r"^(#{1,6})\s+(\S.*)$", text)
				if not m: continue
				level = m.group(1)
				words = m.group(2)
				children = text_to_textnodes(words)
				leaf_children = [text_node_to_html_node(tn) for tn in children]
				p_node = HTMLNode(f"h{len(level)}", None, leaf_children)
				node_list.append(p_node)
			case BlockType.UNORDERED_LIST:
				items = []
				for item in text.splitlines():
					line = item.lstrip()
					if line.startswith("- ") and len(line) > 2:
						child_list = text_to_textnodes(line[2:].strip())
						li_children = [text_node_to_html_node(tn) for tn in child_list]
						items.append(HTMLNode("li", None, li_children))
					else: continue
				node_list.append(HTMLNode("ul", None, items))
			case BlockType.QUOTE:
				print("QUOTE BLOCK:", repr(text))
				items = []
				lines = []
				for raw in text.splitlines():
					line = raw.lstrip()
					if line.startswith(">"):
						text = line[1:]
						if text.startswith(" "): text = text[1:]

						if text.strip() == "":
							if lines:
								text = " ".join(lines).strip()
								tns = text_to_textnodes(text)
								items.append(HTMLNode("p", None, [text_node_to_html_node(tn) for tn in tns]))
								lines = []
						else: lines.append(text)
				if lines:
					text = " ".join(lines).strip()
					tns = text_to_textnodes(text)
					items.append(HTMLNode("p", None, [text_node_to_html_node(tn) for tn in tns]))
				if items and items[0].tag== "p":
					first_children = items[0].children
					rest = items[1:]
					node_list.append(HTMLNode("blockquote", None, first_children + rest))
				else:
					node_list.append(HTMLNode("blockquote", None, items))
			case BlockType.ORDERED_LIST:
				items = []
				for raw in text.splitlines():
					dot_index = raw.find(". ")
					line = raw[dot_index+2:].strip()
					if not line: continue
					tns = text_to_textnodes(line)
					li_children = [text_node_to_html_node(tn) for tn in tns]
					items.append(HTMLNode("li", None, li_children))
				node_list.append(HTMLNode("ol", None, items))
			case _:
				norm = " ".join(line.strip() for line in text.splitlines())
				if not norm: continue
				tn_list = text_to_textnodes(norm)
				leaf_children = [text_node_to_html_node(tn) for tn in tn_list]
				p_node = HTMLNode("p", None, leaf_children)
				node_list.append(p_node)
	return HTMLNode("div", None, node_list, None)
