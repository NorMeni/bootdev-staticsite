import os
import shutil

def copystatic(source_dir, destination):
	if not os.path.exists(source_dir) or not os.path.isdir(source_dir):
		raise Exception(f"{source_dir} path not found.")
	elif os.path.exists(destination):
		shutil.rmtree(destination)
		os.mkdir(destination)
	else: os.mkdir(destination)

	for name in os.listdir(source_dir):
		src_path = os.path.join(source_dir, name)
		dst_path = os.path.join(destination, name)
		if os.path.isdir(src_path):
			os.mkdir(dst_path)
			copystatic(src_path, dst_path)
		elif os.path.isfile(src_path):
			shutil.copy(src_path, dst_path)
			print(f"copied {dst_path}")
