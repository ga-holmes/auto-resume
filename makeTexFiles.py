# Python program to read
# json file
 
import json
import russelFormat as rf
import os

# put in function so it's call-able by other scripts
def makeTexFiles():

    tex_path = "CVout"
    resume_path = "texFiles"

    if not os.path.exists(tex_path):
        os.makedirs(tex_path)
    
    # Opening JSON file
    with open('resumeData.json', 'r', encoding='utf-8') as f:
        # returns JSON object as a dictionary
        data = json.load(f)
    
    # Opening options JSON file
    with open('resumeOptions.json', 'r', encoding='utf-8') as of:
        options = json.load(of)

    # filter sections to only include elements with keywords
    exp_obj = data['work-experience'] # by deafault, set to entire list of objects
    proj_obj = data['projects'] # by deafault, set to entire list of objects
    vol_obj = data['volunteer-experience'] # by deafault, set to entire list of objects

    # only do this if there are some keywords
    if len(options['keywords']) > 0:

        exp_obj = [] # clear the object
        proj_obj = [] # clear the object
        vol_obj = [] # clear the object

        # create sublist of data with relevant points
        for k in options['keywords']:
            
            # items in the lists are converted to lowercase for comparison (NOTE: slow?)
            for w in data['work-experience']:
                if k.lower() in (item.lower() for item in w['relevant-skills']):
                    exp_obj.append(w)

            for w in data['projects']:
                if k.lower() in (item.lower() for item in w['relevant-skills']):
                    proj_obj.append(w)

            for w in data['volunteer-experience']:
                if k.lower() in (item.lower() for item in w['relevant-skills']):
                    vol_obj.append(w)


    # file for basic information - goes into /texFiles directory since it is imported seperately from other files in resume.tex
    info_str = rf.add_cv_info(data['first-name'], data['last-name'], 
                            location=data['location'],
                            phone=data['phone'],
                            email=data['email'],
                            linkedIn=data['linkedIn'],
                            website=data['website'],
                            github=data['github']
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

    # list by order specified in resumeOptions.json
    for f in options['sections-to-include']:

        # do not include sections that are empty due to keywords
        if f == 'experience' and len(exp_obj) > 0:
            import_str += rf.add_import(f + ".tex")
        elif f == 'projects' and len(proj_obj) > 0:
            import_str += rf.add_import(f + ".tex")
        elif f == 'volunteer' and len(vol_obj) > 0:
            import_str += rf.add_import(f + ".tex")
        elif f != 'experience' and f != 'projects' and f != 'volunteer':
            import_str += rf.add_import(f + ".tex")


    with open(os.path.join( resume_path, 'inputs.tex'), 'w') as inputs_out:
        inputs_out.write(import_str)

    return 1


# run the above function
makeTexFiles() 
