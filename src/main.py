from textnode import TextNode
from copystatic import copystatic
from gencontent import *

def main():
	source_dir = "static"
	destination = "public"

	from_path = "content"
	template_path = "template.html"
	dest_path = "public"

	copystatic(source_dir, destination)
	generate_pages_recursive(from_path, template_path, dest_path)

if __name__ == "__main__":
	main()
