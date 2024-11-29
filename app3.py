import streamlit as st
import pdfkit
from jinja2 import Template

# HTML Template for resume
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            color: #333;
        }
        h1 {
            font-size: 28px;
            color: #007ACC;
        }
        p, li {
            font-size: 16px;
            line-height: 1.5;
        }
        .section {
            margin-bottom: 20px;
        }
        .section-title {
            font-size: 20px;
            font-weight: bold;
            color: #444;
            border-bottom: 2px solid #007ACC;
            margin-bottom: 10px;
            padding-bottom: 5px;
        }
        ul {
            list-style-type: disc;
            margin-left: 20px;
        }
    </style>
</head>
<body>
    <h1>{{ name }}</h1>
    <p><strong>Email:</strong> {{ email }}</p>
    <p><strong>Phone:</strong> {{ phone }}</p>
    
    <div class="section">
        <div class="section-title">Objective</div>
        <p>{{ objective }}</p>
    </div>
    
    <div class="section">
        <div class="section-title">Skills</div>
        <ul>
            {% for skill in skills %}
            <li>{{ skill }}</li>
            {% endfor %}
        </ul>
    </div>
    
    <div class="section">
        <div class="section-title">Experience</div>
        {% for job in experience %}
        <p><strong>{{ job.title }}</strong> at {{ job.company }} ({{ job.years }})</p>
        <p>{{ job.description }}</p>
        {% endfor %}
    </div>
    
    <div class="section">
        <div class="section-title">Education</div>
        {% for edu in education %}
        <p><strong>{{ edu.degree }}</strong> from {{ edu.institution }} ({{ edu.year }})</p>
        <p>CGPA: {{ edu.cgpa }}</p>
        {% endfor %}
    </div>
</body>
</html>
"""

# Function to generate PDF
def generate_pdf(html_content):
    try:
        pdf_data = pdfkit.from_string(html_content, False)
        return pdf_data
    except Exception as e:
        st.error(f"Error generating PDF: {e}")
        return None

# Streamlit app
st.title("Resume Generator")

# User inputs
st.header("Enter Your Details")
name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
objective = st.text_area("Objective")
skills = st.text_area("Skills (comma-separated)").split(",")

# Experience Section
st.subheader("Work Experience")
experience = []
for i in range(2):  # Allow up to 2 experiences
    with st.expander(f"Experience {i + 1}"):
        title = st.text_input(f"Job Title {i + 1}", key=f"title_{i}")
        company = st.text_input(f"Company {i + 1}", key=f"company_{i}")
        years = st.text_input(f"Years Worked (e.g., 2020-2023) {i + 1}", key=f"years_{i}")
        description = st.text_area(f"Description {i + 1}", key=f"description_{i}")
        if title and company:
            experience.append({"title": title, "company": company, "years": years, "description": description})

# Education Section
st.subheader("Education")
education = []
for i in range(2):  # Allow up to 2 education entries
    with st.expander(f"Education {i + 1}"):
        degree = st.text_input(f"Degree {i + 1}", key=f"degree_{i}")
        institution = st.text_input(f"Institution {i + 1}", key=f"institution_{i}")
        year = st.text_input(f"Year (e.g., 2023) {i + 1}", key=f"year_{i}")
        cgpa = st.text_input(f"CGPA {i + 1}", key=f"cgpa_{i}")
        if degree and institution:
            education.append({"degree": degree, "institution": institution, "year": year, "cgpa": cgpa})

# Preview Resume
if st.button("Preview Resume"):
    template = Template(TEMPLATE)
    html_content = template.render(
        name=name,
        email=email,
        phone=phone,
        objective=objective,
        skills=[skill.strip() for skill in skills if skill.strip()],
        experience=experience,
        education=education,
    )
    st.markdown(f"""
        <iframe srcdoc="{html_content}" width="100%" height="500px" style="border: none;"></iframe>
    """, unsafe_allow_html=True)

# Generate PDF
if st.button("Generate PDF"):
    template = Template(TEMPLATE)
    html_content = template.render(
        name=name,
        email=email,
        phone=phone,
        objective=objective,
        skills=[skill.strip() for skill in skills if skill.strip()],
        experience=experience,
        education=education,
    )
    pdf_data = generate_pdf(html_content)
    if pdf_data:
        st.download_button(
            label="Download Resume",
            data=pdf_data,
            file_name="resume.pdf",
            mime="application/pdf"
        )
