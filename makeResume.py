import os
from makeTexFiles import *

# call makeTexFiles.py
makeTexFiles(keywords_args=keyword_args(), exclude=exclude_args(), include_all_files=include_all_arg())

# call tex compiler
exec_dir = "./texFiles/"
file = "resume.tex"
cmd = "xelatex"
to_run = cmd + " " + file

# change to new working directory and run latex compiler
os.chdir(exec_dir)

os.system(to_run)