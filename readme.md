# Auto-Resume

This is pretty much an automation project to help me update my resume easily, that said feel free to download it and mess around if you want. 

This program takes CV informaton from a JSON file and compiles it into a defined LaTeX template.
`makeResume.py` contains code that reads data from `resumeData.json` and writes it to files according to a format defined in (for this example) `russelFormat.py`, which contains functions that map the JSON data to string outputs for the format defined in `texFiles/russell.cls`.
I encourage anyone who likes this idea to implement other LaTeX formats that can read and compile the information in `resumeData.json`.

### Next Steps
- Standardize `makeResume.py`, options in a JSON or XML file.
- Implement more LaTeX formats.
- Allow user to specify which format to use in the settings file.

### Credit
The russell class is available on its own at https://github.com/themagicalmammal/Resume, all credit for the latex class and the base `resume.tex` file goes to the contributors to that repository.
- View on overleaf: https://www.overleaf.com/latex/templates/russelresume/zqnypvvjsfvq

* this is not a forked repository since the .tex files & definitions are intended to be an example for using this format to add more LaTeX resume templates.

### Requirements

Python 3.x must be installed on your computer

To compile your finised files, install a LaTeX compiler for your system. I am using MiKTeX due to its small size:
    - Install: https://miktex.org/

### Filling in the JSON
`resumeData.json` is currently filled with my personal CV information as an example (feel free to hire me). You can test the file generation with this, or fill in your own information.
`resumeDataFormat.json` contains JSON in the same fomat as `resumeData.json` but with blank entries. You can either copy this and fill in your information, or use it as a guideline. Be careful not to make any changes to the format of the JSON files without ensuring the change is represented in each one, and that it won't mess with the code in `makeResume.py`.

### Running/Compiling

Step 1:
- run `py makeResume.py`
- The .tex files should be created and put in `/CVout`

Step 2:
- navigate to text folder: `cd texFiles`
- run `xelatex resume.tex`
    - If this is your first time running, MiKTeX will need to install all requirements. I recommend un-checking "show me every time" as there are a lot of packages and it'll get annyoying OK-ing each one.
    - You may be able to compile with other LaTeX commands/formats. `pdflatex` did not work for me so I use `xelatex`.

