from textnode import TextNode
from copystatic import copystatic
from gencontent import *
import sys

def main():
	basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
	if not basepath.endswith("/"):
		basepath += "/"

	source_dir = "static"
	destination = "docs"

	from_path = "content"
	template_path = "template.html"
	dest_path = "docs"

	print("ARGV:", sys.argv)
	print("Basepath before normalize:", sys.argv[1] if len(sys.argv)>1 else "/")

	copystatic(source_dir, destination)
	generate_pages_recursive(from_path, template_path, dest_path, basepath)

if __name__ == "__main__":
	main()
