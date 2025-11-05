class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = [] if children is None else children
		self.props = {} if props is None else props

	def to_html(self):
		if self.tag is None:
			if not self.value: return ""
			return self.value

		attributes = self.props_to_html()
		inner_content = ""

		if self.children:
			for child in self.children:
				inner_content += child.to_html()
		elif self.value is not None:
			inner_content = self.value

		return f"<{self.tag}{attributes}>{inner_content}</{self.tag}>"

	def props_to_html(self):
		result = ""
		if not self.props:
			return ""
		for key, value in self.props.items():
			result += f' {key}="{value}"'
		return result

	def __repr__(self):
		return f"tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value is None:
			raise ValueError()
		if self.tag is None:
			return self.value
		else:
			props = super().props_to_html()
			return f"<{self.tag}{props}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag is None:
			raise ValueError("no tag")
		if self.children is None:
			raise ValueError("no children")
		result = f"<{self.tag}{super().props_to_html()}>"
		for leafnode in self.children:
			result += leafnode.to_html()
		result += f"</{self.tag}>"
		return result
