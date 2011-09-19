""" A collection os useful file utilities """


import os

def file_list(dir):
	""" List the valid python files inside a directory """

	file_list = []

	for f in os.listdir(os.path.abspath(dir)):
		module_name, ext = os.path.splitext(f)
		if ext == '.py': #ignore pycs or other files
			if module_name[0] != '_': #if its not special
				file_list.append(module_name)

	return file_list