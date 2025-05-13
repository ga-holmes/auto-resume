import os
import sys
from makeTexFiles import *

# call makeTexFiles.py
makeTexFiles(keywords_args=keyword_args(), exclude=exclude_args(), include_all_files=include_all_arg())

filename = "resume"

if '-n' in sys.argv:
    i = sys.argv.index('-n')
    if i+1 < len(sys.argv):
        filename = sys.argv[i+1]

# call tex compiler
exec_dir = "./texFiles/"
file = "resume.tex"
cmd = f"xelatex --job-name={filename}"
to_run = cmd + " " + file

# change to new working directory and run latex compiler
os.chdir(exec_dir)

os.system(to_run)

files = os.listdir(".")
for f in files:
    if f.endswith(".tex") or f.endswith(".cls") or f.endswith(".pdf"):
        continue
    else:
        os.remove(os.path.join(".", f))
