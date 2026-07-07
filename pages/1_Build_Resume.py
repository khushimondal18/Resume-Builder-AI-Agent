import streamlit as st

st.title("📝 Build Resume")

if "resume_data" not in st.session_state:
    st.session_state.resume_data = {}

data = st.session_state.resume_data

st.header("1. Personal Information")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Full Name", value=data.get("name", ""))
    degree = st.text_input("Degree / Current Role", value=data.get("degree", ""))
    institute = st.text_input("Institute / University", value=data.get("institute", ""))
    roll_no = st.text_input("Roll No. / ID Optional", value=data.get("roll_no", ""))

with col2:
    email = st.text_input("Email", value=data.get("email", ""))
    phone = st.text_input("Phone", value=data.get("phone", ""))
    linkedin = st.text_input("LinkedIn", value=data.get("linkedin", ""))
    github = st.text_input("GitHub / Portfolio", value=data.get("github", ""))

target_role = st.text_input(
    "Target Job Role",
    value=data.get("target_role", ""),
    placeholder="Software Developer, Data Scientist, UX Designer..."
)

st.divider()

st.header("2. Education")

education_data = data.get("education_data", [])

num_education = st.number_input(
    "How many education entries?",
    min_value=1,
    max_value=6,
    value=max(1, len(education_data)) if education_data else 1
)

education_list = []

for i in range(num_education):
    st.subheader(f"Education {i+1}")
    default = education_data[i] if i < len(education_data) else {}

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        degree_name = st.text_input("Degree / Certificate", value=default.get("degree", ""), key=f"edu_degree_{i}")
    with col2:
        school = st.text_input("Institute / School", value=default.get("institute", ""), key=f"edu_school_{i}")
    with col3:
        score = st.text_input("CGPA / Percentage", value=default.get("score", ""), key=f"edu_score_{i}")
    with col4:
        year = st.text_input("Year", value=default.get("year", ""), key=f"edu_year_{i}")

    if degree_name or school or score or year:
        education_list.append({
            "degree": degree_name,
            "institute": school,
            "score": score,
            "year": year
        })

st.divider()

st.header("3. Experience")

experience_data = data.get("experience_data", [])

num_exp = st.number_input(
    "How many experiences?",
    min_value=0,
    max_value=5,
    value=len(experience_data) if experience_data else 0
)

experience_list = []

for i in range(num_exp):
    st.subheader(f"Experience {i+1}")
    default = experience_data[i] if i < len(experience_data) else {}

    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input("Company / Organization", value=default.get("company", ""), key=f"exp_company_{i}")
        role = st.text_input("Role", value=default.get("role", ""), key=f"exp_role_{i}")

    with col2:
        duration = st.text_input("Duration", value=default.get("duration", ""), key=f"exp_duration_{i}")
        location = st.text_input("Location", value=default.get("location", ""), key=f"exp_location_{i}")

    bullets = st.text_area(
        "Bullet Points",
        value="\n".join(default.get("bullets", [])),
        key=f"exp_bullets_{i}",
        placeholder="- Worked on...\n- Improved...\n- Developed..."
    )

    if company or role or bullets:
        experience_list.append({
            "company": company,
            "role": role,
            "duration": duration,
            "location": location,
            "bullets": [b.strip("-• ").strip() for b in bullets.split("\n") if b.strip()]
        })

st.divider()

st.header("4. Projects")

project_data = data.get("project_data", [])

num_projects = st.number_input(
    "How many projects?",
    min_value=0,
    max_value=8,
    value=len(project_data) if project_data else 1
)

project_list = []

for i in range(num_projects):
    st.subheader(f"Project {i+1}")
    default = project_data[i] if i < len(project_data) else {}

    col1, col2 = st.columns(2)

    with col1:
        project_name = st.text_input("Project Name", value=default.get("name", ""), key=f"project_name_{i}")
        tech_stack = st.text_input("Tech Stack", value=default.get("tech_stack", ""), key=f"project_stack_{i}")

    with col2:
        project_link = st.text_input("Project Link / GitHub", value=default.get("link", ""), key=f"project_link_{i}")
        project_duration = st.text_input("Duration", value=default.get("duration", ""), key=f"project_duration_{i}")

    bullets = st.text_area(
        "Project Bullet Points",
        value="\n".join(default.get("bullets", [])),
        key=f"project_bullets_{i}",
        placeholder="- Built...\n- Implemented...\n- Achieved..."
    )

    if project_name or tech_stack or bullets:
        project_list.append({
            "name": project_name,
            "tech_stack": tech_stack,
            "link": project_link,
            "duration": project_duration,
            "bullets": [b.strip("-• ").strip() for b in bullets.split("\n") if b.strip()]
        })

st.divider()

st.header("5. Technical Skills")

col1, col2 = st.columns(2)

with col1:
    programming = st.text_input("Programming Languages", value=data.get("programming", ""))
    frameworks = st.text_input("Frameworks / Libraries", value=data.get("frameworks", ""))
    databases = st.text_input("Databases", value=data.get("databases", ""))

with col2:
    tools = st.text_input("Tools", value=data.get("tools", ""))
    cloud = st.text_input("Cloud / Platforms", value=data.get("cloud", ""))
    soft_skills = st.text_input("Soft Skills", value=data.get("soft_skills", ""))

st.divider()

st.header("6. Key Courses Taken")

courses = st.text_area(
    "Courses",
    value=data.get("courses", ""),
    placeholder="Data Structures, DBMS, Linear Algebra, Machine Learning..."
)

st.divider()

st.header("7. Achievements")

achievements = st.text_area(
    "Achievements",
    value=data.get("achievements", ""),
    placeholder="- Won hackathon...\n- Qualified exam...\n- Selected for..."
)

st.divider()

st.header("8. Positions of Responsibility")

positions = st.text_area(
    "Positions of Responsibility",
    value=data.get("positions", ""),
    placeholder="- Coordinator, Coding Club\n- Design Team Member, Tech Board"
)

st.divider()

st.header("9. Extracurricular Activities")

extra = st.text_area(
    "Extracurricular Activities",
    value=data.get("extra", ""),
    placeholder="- Volunteered in fest...\n- Participated in sports..."
)

if st.button("💾 Save Resume Details"):
    st.session_state.resume_data = {
        "name": name,
        "degree": degree,
        "institute": institute,
        "roll_no": roll_no,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "target_role": target_role,

        "education_data": education_list,
        "experience_data": experience_list,
        "project_data": project_list,

        "programming": programming,
        "frameworks": frameworks,
        "databases": databases,
        "tools": tools,
        "cloud": cloud,
        "soft_skills": soft_skills,

        "courses": courses,
        "achievements": achievements,
        "positions": positions,
        "extra": extra,
    }

    st.success("Resume details saved successfully! Go to Generate Resume.")