import os
from makeTexFiles import *

# call makeTexFiles.py
makeTexFiles()

# call tex compiler
exec_dir = "./texFiles/"
file = "resume.tex"
cmd = "xelatex"
to_run = cmd + " " + file

# change to new working directory and run latex compiler
os.chdir(exec_dir)

os.system(to_run)