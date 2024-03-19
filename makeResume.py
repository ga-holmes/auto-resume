# Python program to read
# json file
 
import json
import russelFormat as rf
import os

tex_path = "CVout"
if not os.path.exists(tex_path):
    os.makedirs(tex_path)
 
# Opening JSON file
with open('resumeData.json', 'r', encoding='utf-8') as f:
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
 

# file for basic information
info_str = rf.add_cv_info(data['first-name'], data['last-name'], 
                          location=data['location'],
                          phone=data['phone'],
                          email=data['email'],
                          linkedIn=data['linkedIn'],
                          website=data['website'],
                          github=data['github']
                          )
with open(os.path.join( tex_path, 'info.tex'), 'w') as i_out:
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
experience_la_string = rf.create_cvsection("Work Experience") + rf.create_cventries(data['work-experience'], 'employer', 'title', 'location', 'year', 'points')
with open(os.path.join( tex_path, 'experience.tex'), 'w') as ex_out:
    ex_out.write(experience_la_string)

# Create file for projects
projects_la_string = rf.create_cvsection("Projects") + rf.create_cventries(data['projects'], 'title', 'description', 'location', 'year', 'points')
with open(os.path.join( tex_path, 'projects.tex'), 'w') as p_out:
    p_out.write(projects_la_string)

# Create file for volunteer experience
volunteer_la_string = rf.create_cvsection("Volunteer Experience") + rf.create_cventries(data['volunteer-experience'], 'organization', 'title', 'location', 'year', 'points')
with open(os.path.join( tex_path, 'volunteer.tex'), 'w') as v_out:
    v_out.write(volunteer_la_string)

# Create file for skills
skills_la_string = rf.create_cvsection("Skills") + rf.create_cvskills(data['skills'], 'type', 'list')
with open(os.path.join( tex_path, 'skills.tex'), 'w') as sk_out:
    sk_out.write(skills_la_string)

# Create file for certifications
certs_str = rf.create_cvsubsection("Certifications") + rf.create_cvskills(data['certifications'], 'type', 'list')
with open(os.path.join( tex_path, 'certs.tex'), 'w') as c_out:
    c_out.write(certs_str)

# Create file for awards
award_str = rf.create_cvsection("Achievments") + rf.create_cvhonors(data["achievements"], 'award', 'event', 'location', 'year')
with open(os.path.join( tex_path, 'achievements.tex'), 'w') as a_out:
    a_out.write(award_str)

# make list of things to import
    
import_str = ""

for f in os.listdir('Cvout'):
    import_str += "\\input{../CVout/" + f + "}\n"

with open(os.path.join( 'texFiles', 'inputs.tex'), 'w') as inputs_out:
    inputs_out.write(import_str)