from textnode import TextNode

def main():
	node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
	print(repr(node))

if __name__ == "__main__":
	main()
