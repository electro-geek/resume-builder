#!/usr/bin/env python3

import os
import subprocess
import re
from jinja2 import Environment, FileSystemLoader

# A dictionary to hold all the resume data
resume_data = {}

def escape_latex_special_chars(text):
    """
    Escapes special LaTeX characters in a given string.
    """
    if not isinstance(text, str):
        return text
    # Order matters here. '\' must be escaped first.
    conv = {
        '\\': r'\\',
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
    regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key=lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)

def get_user_input(prompt):
    """Gets a single line of input from the user."""
    return input(f"Enter your {prompt}: ")

def get_list_input(prompt):
    """Gets a list of inputs from the user."""
    items = []
    print(f"Enter {prompt} (one item per line). Press Enter on an empty line to finish:")
    while True:
        item = input("> ")
        if not item:
            break
        items.append(item)
    return items

def collect_personal_info():
    """Collects personal information."""
    print("\n--- Personal Information ---")
    resume_data['name'] = get_user_input("Full Name")
    resume_data['location'] = get_user_input("City, Country (e.g., Jaipur, India)")
    resume_data['phone'] = get_user_input("Phone Number")
    resume_data['email'] = get_user_input("Email Address")
    resume_data['portfolio'] = get_user_input("Portfolio/Website URL")
    resume_data['linkedin'] = get_user_input("LinkedIn Profile URL")
    resume_data['github'] = get_user_input("GitHub Profile URL")

def collect_summary():
    """Collects the professional summary."""
    print("\n--- Professional Summary ---")
    print("Enter your professional summary (a few sentences). Press Ctrl+D (Unix) or Ctrl+Z (Windows) then Enter when done.")
    summary_lines = []
    try:
        while True:
            line = input()
            summary_lines.append(line)
    except EOFError:
        pass
    resume_data['summary'] = ' '.join(summary_lines)

def collect_technical_skills():
    """Collects technical skills, categorized."""
    print("\n--- Technical Skills ---")
    skills = {}
    categories = [
        "Languages", "Frameworks", "ML frameworks", "DevOps and API Tools", 
        "Tools", "Database"
    ]
    for category in categories:
        user_input = get_user_input(f"{category} (comma-separated)")
        if user_input:
            skills[category] = [skill.strip() for skill in user_input.split(',')]
    resume_data['technical_skills'] = skills

def collect_experience():
    """Collects work experience."""
    print("\n--- Work Experience ---")
    experience = []
    while True:
        print("\nAdding a new work experience entry (or press Enter on the role to skip):")
        role = get_user_input("Role/Title")
        if not role:
            break
        entry = {
            'role': role,
            'company': get_user_input("Company Name"),
            'start_date': get_user_input("Start Date (e.g., May 2025)"),
            'end_date': get_user_input("End Date (e.g., Present)"),
            'description': get_list_input("responsibilities/achievements")
        }
        experience.append(entry)
    resume_data['experience'] = experience

def collect_internships():
    """Collects internship experience."""
    print("\n--- Internships ---")
    internships = []
    while True:
        print("\nAdding a new internship entry (or press Enter on the role to skip):")
        role = get_user_input("Role/Title")
        if not role:
            break
        entry = {
            'role': role,
            'company': get_user_input("Company/Program Name"),
            'start_date': get_user_input("Start Date (e.g., May 2021)"),
            'end_date': get_user_input("End Date (e.g., August 2021)"),
            'description': get_list_input("responsibilities/achievements")
        }
        internships.append(entry)
    resume_data['internships'] = internships

def collect_education():
    """Collects education details."""
    print("\n--- Education ---")
    education = []
    while True:
        print("\nAdding a new education entry (or press Enter on the university name to skip):")
        university = get_user_input("University/Board")
        if not university:
            break
        entry = {
            'university': university,
            'degree': get_user_input("Degree (e.g., B.E. in ECE)"),
            'gpa': get_user_input("GPA/Percentage (e.g., CGPA: 7.1)"),
            'start_date': get_user_input("Start Date (e.g., September 2018)"),
            'end_date': get_user_input("End Date (e.g., June 2022)")
        }
        education.append(entry)
    resume_data['education'] = education

def collect_projects():
    """Collects project details."""
    print("\n--- Projects ---")
    projects = []
    while True:
        print("\nAdding a new project entry (or press Enter on the title to skip):")
        title = get_user_input("Project Title")
        if not title:
            break
        entry = {
            'title': title,
            'tech': get_user_input("Technologies used"),
            'date': get_user_input("Date (e.g., January 2025)"),
            'description': get_list_input("description points")
        }
        projects.append(entry)
    resume_data['projects'] = projects

def collect_publications():
    """Collects publication details."""
    print("\n--- Publications ---")
    publications = []
    while True:
        print("\nAdding a new publication entry (or press Enter on the title to skip):")
        title = get_user_input("Publication Title")
        if not title:
            break
        entry = {
            'title': title,
            'url': get_user_input("URL to the publication"),
            'venue': get_user_input("Venue/Journal (e.g., ISSN: 2582-8436)"),
            'date': get_user_input("Date (e.g., June 2022)"),
            'description': get_list_input("description points")
        }
        publications.append(entry)
    resume_data['publications'] = publications

def sanitize_data(data):
    """Recursively traverses the data and escapes LaTeX special characters."""
    if isinstance(data, dict):
        return {k: sanitize_data(v) for k, v in data.items()}
    if isinstance(data, list):
        return [sanitize_data(i) for i in data]
    if isinstance(data, str):
        return escape_latex_special_chars(data)
    return data

def main():
    """Main function to run the resume builder."""
    print("Welcome to the Python Resume Builder! 📝")
    print("Please fill in the details for your resume.")

    # 1. Collect all data from the user
    collect_personal_info()
    collect_summary()
    collect_technical_skills()
    collect_experience()
    collect_internships()
    collect_education()
    collect_projects()
    collect_publications()
    
    # 2. Sanitize data for LaTeX
    sanitized_resume_data = sanitize_data(resume_data)

    # 3. Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('.'), autoescape=False)
    template = env.get_template('template.tex')
    
    # 4. Render the template with user data
    output_from_template = template.render(sanitized_resume_data)
    
    # 5. Write the rendered LaTeX to a .tex file
    output_filename_base = "resume"
    tex_filename = f"{output_filename_base}.tex"
    with open(tex_filename, "w", encoding="utf-8") as fh:
        fh.write(output_from_template)
        
    print(f"\n✅ '{tex_filename}' has been created.")
    
    # 6. Compile the .tex file to a PDF using pdflatex
    print("Compiling to PDF... this may take a moment. ⏳")
    try:
        # We run it twice to ensure all references (if any) are correctly generated.
        for i in range(2):
            process = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_filename],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        print(f"✅ Success! Your resume has been generated as '{output_filename_base}.pdf'. 🎉")
    except FileNotFoundError:
        print("\n❌ Error: 'pdflatex' command not found.")
        print("Please ensure you have a LaTeX distribution (like MiKTeX, TeX Live, or MacTeX) installed and in your system's PATH.")
        return
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during PDF compilation. LaTeX returned a non-zero exit code: {e.returncode}")
        print("Please check the 'resume.log' file for detailed LaTeX errors.")
        print("\n--- LaTeX Output ---")
        print(e.stdout.decode('utf-8', errors='ignore'))
        return
    finally:
        # 7. Clean up auxiliary files
        extensions_to_clean = ['.aux', '.log', '.out']
        for ext in extensions_to_clean:
            if os.path.exists(output_filename_base + ext):
                os.remove(output_filename_base + ext)

if __name__ == "__main__":
    main()