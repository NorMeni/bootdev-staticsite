from textnode import *
from htmlnode import *
import os
from pathlib import Path

def extract_title(markdown):
	for line in markdown.splitlines():
		if line.startswith("# "):
			title = line[2:].strip()
			if title:
				return title
	raise Exception("h1 header not found")

def generate_page(from_path, template_path, dest_path, basepath):
	print(f"Generating a page {from_path} to {dest_path} using {template_path}")
	with open(from_path, "r", encoding="utf-8") as f:
		from_string = f.read()
	with open(template_path, "r", encoding="utf-8") as f:
		template_string = f.read()

	content_html = markdown_to_html_node(from_string).to_html()
	title = extract_title(from_string)

	print("Replacing with basepath:", basepath)
	print("Template contains href? ", 'href="/' in template_string)

	page_html = template_string.replace("{{ Title }}", title)
	page_html = page_html.replace("{{ Content }}", content_html)

	page_html = page_html.replace('href="/', f'href="{basepath}')
	page_html = page_html.replace('src="/', f'src="{basepath}')

	dest_dir = os.path.dirname(dest_path)
	if dest_dir:
		os.makedirs(dest_dir, exist_ok=True)

	with open(dest_path, "w", encoding="utf-8") as f:
		f.write(page_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
	entry_list = os.listdir(dir_path_content)
	for entry in entry_list:
		if os.path.isfile(os.path.join(dir_path_content, entry)):
			new_dest = Path(os.path.join(dest_dir_path, entry)).with_suffix(".html")
			os.makedirs(os.path.dirname(new_dest), exist_ok=True)
			generate_page(os.path.join(dir_path_content, entry), template_path, new_dest, basepath)
		else:
			os.makedirs(os.path.join(dest_dir_path, entry), exist_ok=True)
			generate_pages_recursive(os.path.join(dir_path_content, entry), template_path, os.path.join(dest_dir_path, entry), basepath)
