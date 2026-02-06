# Python program to read
# json file
 
import json
import russelFormat as rf
import os
import sys

reserved_cmd = ['-k', '-e', '-a', '-n', '-d']

# searches sys.argv for '-k' and returns a new list starting at that position
def keyword_args():

    start = 0

    for i, a in enumerate(sys.argv):
        if a == "-k":
            start = i
        elif a in reserved_cmd and start > 0:
            i -= 1 # to remove from list
            break
        

    if start > 0:
        return sys.argv[start:i+1]

    return []

# check which args exclude
def exclude_args():
    start = 0

    for i, a in enumerate(sys.argv):
        if a == "-e":
            start = i + 1
        elif a in reserved_cmd and start > 0:
            i -= 1 # to remove from list
            break
        

    if start > 0:
        return sys.argv[start:i+1]

    return []

# check argv for '-a'
def include_all_arg():
    return ('-a' in sys.argv)

def latex_escape(s: str) -> str:
    replacements = {
        '\\': r'\textbackslash{}',
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    return s


def latex_sanitize(obj):
    if isinstance(obj, str):
        return latex_escape(obj)
    elif isinstance(obj, list):
        return [latex_sanitize(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: latex_sanitize(v) for k, v in obj.items()}
    else:
        return obj


# put in function so it's call-able by other scripts
def makeTexFiles(keywords_args = [], exclude = [], include_all_files = False, resume_data_file="resumeData.json"):

    tex_path = "CVout"
    resume_path = "texFiles"

    if not os.path.exists(tex_path):
        os.makedirs(tex_path)
    
    # Opening options JSON file
    with open('resumeOptions.json', 'r', encoding='utf-8') as of:
        options = json.load(of)
    
    # get data file path if specified
    if "data-file-path" in options:
        resume_data_file = options["data-file-path"]

    # Opening JSON file
    with open(resume_data_file, 'r', encoding='utf-8') as f:
        # returns JSON object as a dictionary
        raw_data = json.load(f)

    data = latex_sanitize(raw_data)
    
    # filter sections to only include elements with keywords
    exp_obj = data['work-experience'] # by deafault, set to entire list of objects
    proj_obj = data['projects'] # by deafault, set to entire list of objects
    vol_obj = data['volunteer-experience'] # by deafault, set to entire list of objects

    keywords = options['keywords']

    # overwrite keywords if args is not empty
    if len(keywords_args) > 0:
        keywords = keywords_args[1:]

    # only do this if there are some keywords
    if len(keywords) > 0:

        exp_obj = [] # clear the object
        proj_obj = [] # clear the object
        vol_obj = [] # clear the object

        # create sublist of data with relevant points
        for k in keywords:
            
            # items in the lists are converted to lowercase for comparison (NOTE: slow?)
            for w in data['work-experience']:
                if any(k.lower() == item.lower() and w not in exp_obj for item in w['relevant-skills']):
                    exp_obj.append(w)

            for w in data['projects']:
                if any(k.lower() == item.lower() and w not in proj_obj for item in w['relevant-skills']):
                    proj_obj.append(w)

            for w in data['volunteer-experience']:
                if any(k.lower() == item.lower() and w not in vol_obj for item in w['relevant-skills']):
                    vol_obj.append(w)

    # if any are empty, do not include on resume
    if len(exp_obj) < 1: exclude.append('experience')
    if len(proj_obj) < 1: exclude.append('projects')
    if len(vol_obj) < 1: exclude.append('volunteer')
    if len(data['skills']) < 1: exclude.append('skills')
    if len(data['certifications']) < 1: exclude.append('certifications')
    if len(data['education']) < 1: exclude.append('education')
    if len(data['achievements']) < 1: exclude.append('achievements')

    # file for basic information - goes into /texFiles directory since it is imported seperately from other files in resume.tex
    info_str = rf.add_cv_info(data['first-name'], data['last-name'], 
                            location=data.get('location'),
                            phone=data.get('phone'),
                            email=data.get('email'),
                            linkedIn=data.get('linkedIn'),
                            website=data.get('website'),
                            github=data.get('github')
                            )
    with open(os.path.join( resume_path, 'info.tex'), 'w') as i_out:
        i_out.write(info_str)

    # file for personal summary
    profile_str = rf.create_cvsection("Summary") + rf.create_cvparagraph(data['summary'])
    with open(os.path.join( tex_path, 'summary.tex'), 'w') as s_out:
        s_out.write(profile_str)

    # Create file for education
    education_la_string = rf.create_cvsection("Education") + rf.create_cventries(data['education'], 'school', 'program', 'location', 'year', 'points', sub_list_key='courses')
    with open(os.path.join( tex_path, 'education.tex'), 'w') as edu_out:
        edu_out.write(education_la_string)

    # Create file for work experience
    experience_la_string = rf.create_cvsection("Work Experience") + rf.create_cventries(exp_obj, 'employer', 'title', 'location', 'year', 'points')
    with open(os.path.join( tex_path, 'experience.tex'), 'w') as ex_out:
        ex_out.write(experience_la_string)

    # Create file for projects
    projects_la_string = rf.create_cvsection("Projects") + rf.create_cventries(proj_obj, 'title', 'description', 'location', 'year', 'points')
    with open(os.path.join( tex_path, 'projects.tex'), 'w') as p_out:
        p_out.write(projects_la_string)

    # Create file for volunteer experience
    volunteer_la_string = rf.create_cvsection("Volunteer Experience") + rf.create_cventries(vol_obj, 'organization', 'title', 'location', 'year', 'points')
    with open(os.path.join( tex_path, 'volunteer.tex'), 'w') as v_out:
        v_out.write(volunteer_la_string)

    # Create file for skills
    skills_la_string = rf.create_cvsection("Skills") + rf.create_cvskills(data['skills'], 'type', 'list')
    with open(os.path.join( tex_path, 'skills.tex'), 'w') as sk_out:
        sk_out.write(skills_la_string)

    # Create file for certifications
    certs_str = rf.create_cvskills(data['certifications'], 'type', 'list')
    with open(os.path.join( tex_path, 'certs.tex'), 'w') as c_out:
        c_out.write(certs_str)

    # Create file for awards
    award_str = rf.create_cvsection("Achievments") + rf.create_cvhonors(data["achievements"], 'award', 'event', 'location', 'year')
    with open(os.path.join( tex_path, 'achievements.tex'), 'w') as a_out:
        a_out.write(award_str)


    # make list of things to import organized by filename
        
    import_str = ""

    # alphabetical in this case
    if len(options['sections-to-include']) < 1 or include_all_files:

        for f in os.listdir(tex_path):
            # exclude sections in the 'exclude' list
            if f not in exclude:
                import_str += rf.add_import(f + ".tex")

    else:

        # list by order specified in resumeOptions.json
        for f in options['sections-to-include']:

            # exclude sections in the 'exclude' list
            if f not in exclude:
                import_str += rf.add_import(f + ".tex")


    with open(os.path.join( resume_path, 'inputs.tex'), 'w') as inputs_out:
        inputs_out.write(import_str)

    return 1


# Defining main function 
def main(): 
    makeTexFiles(keywords_args=keyword_args(), exclude=exclude_args(), include_all_files=include_all_arg())
  
  
# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 
