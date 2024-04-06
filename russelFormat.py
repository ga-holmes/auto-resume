
# maybe implement later
# def indent_str(indent):
#     tab_str = ""
#     for i in range(0, indent):
#         tab_str += "\t"

#     return tab_str

# basic information - set in JSON
def add_cv_info(first_name, last_name, location="", phone="", email="", linkedIn="", website="", github=""):
   out_str = ""

   out_str += f"\\name{{{first_name}}}{{{last_name}}}\n"
   out_str += f"\\address{{{location}}}\n"
   out_str += f"\\mobile{{{phone}}}\n"
   out_str += f"\\email{{{email}}}\n"
   out_str += f"\\homepage{{{website}}}\n"
   out_str += f"\\github{{{github}}}\n"
   out_str += f"\\linkedin{{{linkedIn}}}\n"

   return out_str

# add a header
def create_cvsection(title):
    return f"\n\\cvsection{{{title}}}\n"

def create_cvsubsection(title):
    return f"\n\\cvsubsection{{{title}}}\n"

def create_cvparagraph(content):
   return f"\n\\begin{{cvparagraph}}\n{content}\n\\end{{cvparagraph}}\n"

def create_cventries(entry_list, title_key, description_key, location_key, dates_key, notes_list_key, sub_list_key = ''):
    out_str = "\n\\begin{cventries}\n"

    for e in entry_list:
        if sub_list_key == '':
          out_str += create_cventry(e[title_key], e[description_key], e[location_key], e[dates_key], e[notes_list_key])
        else:
          out_str += create_cventry(e[title_key], e[description_key], e[location_key], e[dates_key], e[notes_list_key], e[sub_list_key], sub_list_key=sub_list_key)
    
    out_str += "\n\\end{cventries}"

    return out_str

def create_cventry(title, description, location, dates, notes_list, sub_list = [], sub_list_key = ''):

    # triple brackets to get {} in f-string
    out_str = f"\n\n\\cventry\n{{{description}}}\n{{{title}}}\n{{{location}}}\n{{{dates}}}"

    # add cvitems
    if (len(notes_list) > 0):
        out_str += create_cvitems(notes_list, sub_list, sub_list_key=sub_list_key)

    return out_str

def create_cvitems(item_list, sub_list = [], sub_list_key = ''):

    # begin cvitems entry
    out_str = "\n{\n\\begin{cvitems}"

    for n in item_list:
      out_str += "\n"
      out_str += f"\\item {{{n}}}"

    if sub_list_key != '' and len(sub_list) > 0:
      out_str += create_bold_cvitem(sub_list, sub_list_key)
    
    out_str += f"\n\\end{{cvitems}}\n" + "}"

    return out_str

def create_bold_cvitem(sub_list, sub_list_key):
    
    out_str = "\n\\item {\\textbf{" + sub_list_key.title() + ":}"

    for n in sub_list:
      out_str += f" {n},"

    # remove trailing comma
    out_str = out_str.rstrip(',') 
    
    out_str += "}"

    return out_str

def create_cvhonors(entry_list, award_key, event_key, location_key, dates_key):
    out_str = "\n\\begin{cvhonors}\n"

    for e in entry_list:
      out_str += f"\\cvhonor\n{{{e[award_key]}}}\n{{{e[event_key]}}}\n{{{e[location_key]}}}\n{{{e[dates_key]}}}"
    
    out_str += "\n\\end{cvhonors}"

    return out_str

def create_cvskills(skills_list, category_key, list_key):
  out_str = "\n\\begin{cvskills}\n"

  for c in skills_list:
    out_str += create_cvskill(c[category_key], c[list_key])

  out_str += "\n\\end{cvskills}"

  return out_str

def create_cvskill(category, skills):
  out_str = f"\n\\cvskill\n{{{category}}}\n" + "{"

  for s in skills:
      out_str += f" {s},"
    
  # remove trailing comma
  out_str = out_str.rstrip(',')
  
  out_str += "}\n"

  return out_str

# add citable articles - pub_list contains the names of publications that are part of an accessible references.bib file
def create_bibliography(pub_list):
   
  out_str = "\n\\begin{refsection}\n"

  for p in pub_list:
    out_str += f"\\nocite{{{p}}}\n"

  out_str += "\\newrefcontext[sorting=ydnt]\n\\printbibliography[heading=none]\n\\end{refsection}"  
